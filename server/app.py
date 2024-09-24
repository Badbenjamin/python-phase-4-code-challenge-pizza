#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


@app.route('/restaurants')
def get_restaurants():
    return [restaurant.to_dict(only=('address', 'id', 'name')) for restaurant in Restaurant.query.all()], 200

@app.route('/restaurants/<int:id>')
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()
    return restaurant.to_dict(), 200
    

if __name__ == "__main__":
    app.run(port=5555, debug=True)
