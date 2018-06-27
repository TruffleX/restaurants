from collections import Counter
from tqdm import tqdm_notebook
import time
from spacy.matcher import PhraseMatcher
import spacy
from db.dbclient import MongoClient


class RestaurantAnnotator:

    def __init__(self):

        self._nlp = spacy.blank('en')
        self._nlp.add_pipe(self._nlp.create_pipe('sentencizer'))

        self.matcher = PhraseMatcher(self._nlp.tokenizer.vocab, max_length=10)
        phrases = self._build_gazateer()
        for phrase in phrases:
            self.matcher.add(phrase.text, None, phrase)


    def _build_gazateer(self):
        restaurant_iter = MongoClient('restaurant').collection.find({})
        phrases = self._read_gazateer(self._nlp.tokenizer, restaurant_iter)
        return phrases

    def _read_gazateer(self, tokenizer, restaurant_iter):
        names = map(lambda x: x.get('name'), restaurant_iter)
        for i, name in enumerate(names):
            phrase = tokenizer(name)
            for w in phrase:
                _ = tokenizer.vocab[w.text]
            if len(phrase) >= 1 and len(phrase) < 10:
                yield phrase

    def annotate_text(self, text):
        doc = self._nlp(text)
        for w in doc:
            _ = doc.vocab[w.text]
        matches = self.matcher(doc)
        for ent_id, start, end in matches:
            yield (ent_id, doc[start:end].text)

    def annotate_article(self, article, method='most-consistent'):
        sections = ['content', 'title', 'meta_description']
        texts = {section: article.get(section, " ") for section in sections}
        matches = {section: Counter() for section in sections}

        for section in sections:
            text = texts[section]
            doc = self._nlp(text)
            for w in doc:
                _ = doc.vocab[w.text]
            for sent in doc.sents:
                sent_doc = self._nlp.tokenizer(sent.text)

                match_results = self.matcher(sent_doc)
                matched, longest = None, 0

                for ent_id, start, end in match_results:
                    string = self._nlp.vocab.strings[ent_id]
                    if len(string) > longest:
                        longest = len(string)
                        matched = string

                    matches[section][string] += 1

        result = {
            'text': texts,
            'matches': matches,
            'is_review_score': article['is_review_score']
        }

        methods = {
            "most-common": self._most_common,
            "most-consistent": self._most_consistent,
        }

        return methods.get(method, self._most_common)(result)

    def _most_common(self, result):
        all_counts = Counter()
        for section, counter in result['matches'].items():
            for word, count in counter.items():
                all_counts[word] += count

        most_common = all_counts.most_common(1)

        if most_common:
            pick, count = most_common[0]
            if count > 1:
                result['best_match'] = pick
            else:
                result['best_match'] = None
        else:
            result['best_match'] = None

        return result.get('best_match', None)

    def _most_consistent(self, result):
        print(result['matches'])
        all_counts = Counter()
        for section, counter in result['matches'].items():
            for word, count in counter.items():
                all_counts[word] += 1

        most_common = all_counts.most_common(1)

        if most_common:
            pick, count = most_common[0]
            if count > 1:
                result['best_match'] = pick
            else:
                result['best_match'] = None
        else:
            result['best_match'] = None

        return result.get('best_match', None)
