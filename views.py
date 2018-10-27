#!/usr/bin/env python2
from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

engine = create_engine('sqlite:///restaruants.db?check_same_thread=False')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
    # Return all restaurants on file
    if request.method == 'GET':
       restaurants = session.query(Restaurant).all()
       return jsonify(restaurants=[i.serialize for i in restaurants])
    if request.method == 'POST':
       mealType = request.args.get('mealType', '')
       location = request.args.get('location', '')
       r = findARestaurant(mealType,location)
       if r != None:
         # Error recieved using unicode on following line. I believe it is because I am using Python 3.7.0 and Udacity is using 2.7.12
          restaurant = Restaurant(restaurant_name = unicode(r['name']), restaurant_address = unicode(r['address']), restaurant_image = r['image']) 
          #restaurant = Restaurant(restaurant_name = str(r['name']), restaurant_address = str(r['address']), restaurant_image = r['image'])
          session.add(restaurant)
          session.commit()
          return jsonify(restaurant=restaurant.serialize)
       else:
           return jsonify({"error":"No Restaurants Found for %s in %s" % (mealType, location)}) 
    
@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
    restaurant = session.query(Restaurant).filter_by(id = id).one()
    # Get a restaurant with the ID passed
    if request.method == 'GET':
       return jsonify(restaurant=restaurant.serialize)
    # Update the restaurant with the ID passed
    if request.method == 'PUT':
       name = request.args.get('name', '')
       address = request.args.get('address', '')
       image = request.args.get('image', '')
       if name:
          restaurant.restaurant_name = name
       if address:
          restaurant.restaurant_address = address
       if image:
          restaurant.restaurant_image = image
       session.commit()
       return jsonify(restaurant = restaurant.serialize)
    # Delete the restaurant with the ID passed
    elif request.method == 'DELETE':
         restaurant = session.query(Restaurant).filter_by(id = id).one()
         session.delete(restaurant)
         session.commit()
         return "Removed Restaurant with id %s" % id


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


  
