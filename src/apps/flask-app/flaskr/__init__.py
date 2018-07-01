import os

from flask import Flask, render_template, request, jsonify
from . import database, model
import json
from bson import ObjectId
import pymongo

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
        GOOGLE_MAPS_API_KEY=os.environ['GOOGLE_MAPS_API_KEY']
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

    db_model = model.Model()
    encoder = JSONEncoder()

    from . import database
    database.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    # a simple page that says hello
    @app.route('/')
    def map():
        return render_template('map.html', GOOGLE_MAPS_API_KEY=os.environ['GOOGLE_MAPS_API_KEY'])

    @app.route('/restaurants/filter', methods=['POST'])
    def filter_entries():
        west = float(request.form['west'])
        east = float(request.form['east'])
        north = float(request.form['north'])
        south = float(request.form['south'])
        max_results = int(request.form['max_results'])
        print(request.form)
        restaurant_iter = db_model.restaurants.filter_by_coords(west=west,
                                                                east=east,
                                                                north=north,
                                                                south=south)

        restaurant_iter = restaurant_iter.sort('yelp.rating', pymongo.DESCENDING).limit(max_results)

        return encoder.encode([restaurant for restaurant in restaurant_iter])

    @app.route('/restaurants', methods=['GET'])
    def get_all():
        restaurant_iter = db_model.restaurants.get_all()
        return encoder.encode([restaurant for restaurant in restaurant_iter])

    return app
