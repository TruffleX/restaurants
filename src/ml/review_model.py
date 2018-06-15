from db.dbclient import MongoClient
import numpy as np
from spacy.language import Language
import spacy
from spacy.util import minibatch, compounding
from functools import partial
from sklearn.model_selection import train_test_split
import os
import json


class ReviewModel:

    def __init__(self, model=None):
        self.nlps = {}

    def load_docs(self, field, test_size=.25):
        query = {"is_review": {"$exists": True}}
        client = MongoClient('articles').collection
        results = list(client.find(query))

        texts, labels = [i.get(field, " ") for i in results], [{"is_review": int(i['is_review'])} for i in results]
        return train_test_split(texts, labels, test_size=test_size)

    def make_nlp(self, model=None):
        if model is not None:

            nlp = spacy.load(model)  # load existing spaCy model
            print("Loaded model '%s'" % model)
        else:
            nlp = spacy.load('en')
            print("Created blank 'en' model")

        if 'textcat' not in nlp.pipe_names:
            self.textcat = nlp.create_pipe('textcat')
            nlp.add_pipe(self.textcat, last=True)

        return nlp

    def train(self, model=None, field='content', test_size=.25, n_iter=15, n_texts=2000):

        if model is not None:
            nlp = spacy.load(model)  # load existing spaCy model
            print("Loaded model '%s'" % model)
        else:
            nlp = spacy.load('en')
            print("Created blank 'en' model")

        if 'textcat' not in nlp.pipe_names:
            self.textcat = nlp.create_pipe('textcat')
            nlp.add_pipe(self.textcat, last=True)
        # otherwise, get it, so we can add labels to it
        else:
            self.textcat = nlp.get_pipe('textcat')

            # add label to text classifier
        self.textcat.add_label('is_review')

        train_texts, test_texts, train_labels, test_labels = self.load_docs(field, test_size=test_size)

        # get names of other pipes to disable them during training
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'textcat']
        train_data = list(zip(train_texts,
                              [{'cats': i} for i in train_labels]))

        with nlp.disable_pipes(*other_pipes):  # only train textcat
            optimizer = nlp.begin_training()
            print("Training the model...")
            print('{:^5}\t{:^5}\t{:^5}\t{:^5}'.format('LOSS', 'P', 'R', 'F'))
            for i in range(n_iter):
                try:
                    losses = {}
                    # batch up the examples using spaCy's minibatch
                    batches = minibatch(train_data, size=compounding(4., 32., 1.001))
                    for batch in batches:
                        texts, annotations = zip(*batch)
                        nlp.update(texts, annotations, sgd=optimizer, drop=0.2,
                                   losses=losses)
                    with self.textcat.model.use_params(optimizer.averages):
                        # evaluate on the dev data split off in load_data()
                        scores = self.evaluate(nlp.tokenizer, self.textcat, test_texts, test_labels)
                    print('{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}'  # print a simple table
                          .format(losses['textcat'], scores['textcat_p'],
                                  scores['textcat_r'], scores['textcat_f']))
                except KeyboardInterrupt:
                    break

        return nlp

    def evaluate(self, tokenizer, textcat, texts, cats):
        docs = (tokenizer(text) for text in texts)
        tp = 1e-8  # True positives
        fp = 1e-8  # False positives
        fn = 1e-8  # False negatives
        tn = 1e-8  # True negatives
        for i, doc in enumerate(textcat.pipe(docs)):
            gold = cats[i]
            for label, score in doc.cats.items():
                if label not in gold:
                    continue
                if score >= 0.5 and gold[label] >= 0.5:
                    tp += 1.
                elif score >= 0.5 and gold[label] < 0.5:
                    fp += 1.
                elif score < 0.5 and gold[label] < 0.5:
                    tn += 1
                elif score < 0.5 and gold[label] >= 0.5:
                    fn += 1
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f_score = 2 * (precision * recall) / (precision + recall)
        return {'textcat_p': precision, 'textcat_r': recall, 'textcat_f': f_score}

    def create_model(self, **train_args):
        nlps = {}
        for field in ['title', 'content', 'meta_description']:
            nlp = self.train(field=field, **train_args)
            nlps[field] = nlp
        return nlps

    def build(self, **train_args):
        self.nlps = self.create_model(**train_args)

    def predict(self, document):
        """

        :param document: dict like object with article fields as keys and strings as values
        :return: float in [0, 1]
        """

        def fix(x):
            if x is None:
                return " "
            if x == "":
                return " "
            return x

        if self.nlps is None:
            raise ValueError("call .build first")
        return np.mean([nlp(fix(document.get(key, " "))).cats['is_review'] for key, nlp in self.nlps.items()])

    def save(cls, directory='/home/jovyan/models/review_model'):
        if not os.path.exists(directory):
            os.mkdir(directory)
        info = {}
        for key, model in cls.nlps.items():
            path = os.path.join(directory, f"{key}.mdl")
            model.to_disk(path)
            info[key] = path
        with open(os.path.join(directory, "info.json"), 'w') as f:
            json.dump(info, f)

    def load(self, directory='/home/jovyan/models/review_model'):
        with open(os.path.join(directory, "info.json")) as f:
            info = json.load(f)

        for key, path in info.items():
            nlp = self.make_nlp()
            nlp = nlp.from_disk(path)
            self.nlps[key] = nlp
