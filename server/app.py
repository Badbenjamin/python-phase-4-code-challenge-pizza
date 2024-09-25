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

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()
    if restaurant is None:
        return {"error" : "Restaurant not found"}, 404
    
    if request.method == 'GET':
        return restaurant.to_dict(), 200
    if request.method == 'DELETE':
        db.session.delete(restaurant)
        db.session.commit()
        return {}, 204
    
@app.route('/pizzas')
def get_pizzas():
    return [pizza.to_dict(only=('ingredients', 'id', 'name')) for pizza in Pizza.query.all()], 200

@app.route('/restaurant_pizzas', methods=['POST'])
def post_restaurant_pizza():
    data = request.get_json()
    try:
        new_restaurant_pizza = RestaurantPizza(
            price=data.get('price'),
            pizza_id=data.get('pizza_id'),
            restaurant_id=data.get('restaurant_id')
        )
    except ValueError:
        return {"errors": ["validation errors"]}, 400
    db.session.add(new_restaurant_pizza)
    db.session.commit()
    return new_restaurant_pizza.to_dict(), 201
    

if __name__ == "__main__":
    app.run(port=5555, debug=True)
