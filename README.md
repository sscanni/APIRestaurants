# APIRestaurants

# Overview

```
localhost:5000/restaurants?location=New+York+NY&mealtype=spaghetti
```
* geocodes location
* finds a nearby restaurant
* stores it in a database and returns JSON object
* This is done on a POST request

```
localhost:5000/restaurants
```
* returns all of the restaurants in the database
* return a JSON object with the following:
**{restaurant_name, id, resturant_address, restaurant_image}**
* This is done on a GET request

```
localhost:5000/restaurants/<int: id>
```
* will take in a restuarant's id
* return a JSON object with the following:
**{restaurant_name, id, resturant_address, restaurant_image}**
* This is done on a GET request

```
localhost:5000/restaurants/<int: id>/name=Larry+Burger&location=742+Evergreen+Terrace&image=udacity.com/image.html
```
* will taken in a restuarant's id along with any or all of the names, location and image.
* this should update the information in the database for this id.
* return a JSON object with the following:
**{restaurant_name, id, resturant_address, restaurant_image}**
* This is done on a UPDATE request

```
localhost:5000/restaurants/<int: id>
```
* will take in a restuarant's id
* with a DELETE request
* will delete the restaurant from the database
