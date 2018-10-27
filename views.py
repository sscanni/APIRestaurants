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
    if request.method == 'GET':
       return getAllRestaurant()
    if request.method == 'POST':
       mealType = request.args.get('type', '')
       location = request.args.get('location', '')
       r = findARestaurant(mealType,location)
       return makeANewRestuarant(r['name'],r['address'],r['image'])
    
@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
    if request.method == 'GET':
       return getRestaurant(id)
    if request.method == 'PUT':
       name = request.args.get('name', '')
       location = request.args.get('location', '')
       image = request.args.get('image', '')
       return {'name':name, 'location':location, 'image':image}
    elif request.method == 'DELETE':
         return deleteRestaurant(id)

def getAllRestaurant():
    print ("getAllRestaurant")
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurant=[i.serialize for i in restaurants])

def getRestaurant(id):
    print ("getRestaurant")
    restaurant = session.query(Restaurant).filter_by(id = id).one()
    return jsonify(restaurant=restaurant.serialize)

def makeANewRestuarant(name,address,image):
    restaurant = Restaurant(name = name, address = address, image = image)
    session.add(Restaurant)
    session.commit()
    return jsonify(Restaurant=restaurant.serialize)

def deleteRestaurant(id):
    restaurant = session.query(Restaurant).filter_by(id = id).one()
    session.delete(restaurant)
    session.commit()
    return "Removed Restaurant with id %s" % id

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


  
