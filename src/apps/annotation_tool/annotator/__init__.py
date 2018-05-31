import os

from flask import Flask, render_template, request, jsonify
import json
from bson import ObjectId
from db.dbclient import MongoClient


def prev(obj):
    return obj.__prev__()

class MongoIterator:
    def __init__(self, collection):
        self.i = -1
        self.collection = collection
        ids = collection.find({}, projection=['_id'])
        self.ids = [i['_id'] for i in ids]
    def getter(self, i):
        query = {"_id": self.ids[i]}
        doc = self.collection.find_one(query)
        return doc

    def __iter__(self):
        return self

    def __next__(self):
        self.i += 1
        result = self.getter(self.i)
        return result

    def __prev__(self):
        self.i -= 1
        result = self.getter(self.i)
        return result


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        ML_MODEL_PATH=os.path.join(__file__, '/ml/nlp.mdl'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    encoder = JSONEncoder()
    source_db = MongoClient("articles").collection
    source_iter = MongoIterator(source_db)



    @app.route('/')
    def map():
        doc = next(source_iter)
        return render_template('main.html',
            doc=doc['content'],
            title=doc["title"],
            annotations=doc.get('annotations')
        )

    @app.route('/next')
    def get_next():
        doc = next(source_iter)
        return jsonify({
            "doc": doc.get('content', ""),
            'title': doc.get('title', ""),
            'annotations': doc.get('annotations', []),
        })

    @app.route('/prev')
    def get_prev():
        doc = prev(source_iter)
        return jsonify({
            "doc": doc.get('content', ""),
            'title': doc.get('title', ""),
            'annotations': doc.get('annotations', []),
        })

    return app


def get_next_doc():
    client = MongoClient("articles")
    collection = client.collection
    # find all docs where labels do not exist
    collection.find({ "label": { "$exists": False } })
