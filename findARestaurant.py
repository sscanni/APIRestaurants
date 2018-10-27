from getAPIKeyPackage.getAPIKeys import getAPIKey
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

# Read the google_api_key from a local database
google_api_key = getAPIKey("Google", "GeocodeLocation", "google_api_key")

# Read the client_id and client_secret from a local database
foursquare_client_id = getAPIKey("Foursquare", "Foursquare", "client_id")
foursquare_client_secret = getAPIKey("Foursquare", "Foursquare", "client_secret")

curdate = '20181023'

def getGeocodeLocation(inputString):
    # print ("inputString=%s" % (inputString))
    # print ("google_api_key=%s" % (google_api_key))
    # Use Google Maps to convert a location into Latitute/Longitute coordinates
    # FORMAT: https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=API_KEY
    locationString = inputString.replace(" ", "+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'% (locationString, google_api_key))
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    return (latitude,longitude)

def findARestaurant(mealType,location):
    # print ("mealType=%s" % (mealType))
    # print ("location=%s" % (location))
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    latlong = getGeocodeLocation(location)
    latitude=('{:3.2f}'.format(latlong[0]))
    longitude=('{:3.2f}'.format(latlong[1]))
    latlong = ("%s,%s" % (latitude, longitude))
    # print ("latlong=%s" % (latlong))
    #2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
    url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=%s&ll=%s&query=%s'% (foursquare_client_id, foursquare_client_secret, curdate, latlong, mealType))
    # print ("url=%s" % (url))
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    if result['response']['venues']:
        #3. Grab the first restaurant
        name = result['response']['venues'][0]['name']
        venue_id = result['response']['venues'][0]['id']
        addrLine = ""
        for i in result['response']['venues'][0]['location']['formattedAddress']:
            addrLine += i
            addrLine += " "
	    #4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture        
        url = ('https://api.foursquare.com/v2/venues/%s/photos/?client_id=%s&client_secret=%s&v=%s'% (venue_id, foursquare_client_id, foursquare_client_secret, curdate))
        h = httplib2.Http()
        result = json.loads(h.request(url,'GET')[1])
        #5. Grab the first image
        imageURL = ""
        if result['meta']['code'] == 200:
            if result['response']['photos']['count'] > 0:
                imageURL += result['response']['photos']['items'][0]['prefix']
                imageURL += "300x300"
                imageURL += result['response']['photos']['items'][0]['suffix']
            else:
                #6. If no image is available, insert default a image url
                imageURL = "https://pixabay.com/en/restaurant-wine-glasses-served-449952/"
        else:
            imageURL = "https://pixabay.com/en/restaurant-wine-glasses-served-449952/"
        #7. Return a dictionary containing the restaurant name, address, and image url	
        dict = {'name':name, 'address':addrLine, 'image':imageURL}
        #print ("dict=%s" % (dict))
        return dict
    else: 
        return None
    
def PrintInfo(d):
    if d:
        print ("Restaurant Name: %s" % (d['name']))
        print ("Restaurant Address: %s" % (d['address']))
        print ("Imaage: %s" % (d['imageurl']))
        print 
    else:
        print ("No restaurants found")
    return

if __name__ == '__main__':
    print(findARestaurant("Pizza", "Tokyo, Japan"))
    print(findARestaurant("Tacos", "Jakarta, Indonesia"))
    print(findARestaurant("Tapas", "Maputo, Mozambique"))
    print(findARestaurant("Falafel", "Cairo, Egypt"))
    print(findARestaurant("Spaghetti", "New Delhi, India"))
    print(findARestaurant("Cappuccino", "Geneva, Switzerland"))
    print(findARestaurant("Sushi", "Los Angeles, California"))
    print(findARestaurant("Steak", "La Paz, Bolivia"))
    print(findARestaurant("Gyros", "Sydney Australia"))
