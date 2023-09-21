# Import the required library
from geopy.geocoders import Nominatim

# Initialize Nominatim API
def get_location_name(latitude, longitude):
    geolocator = Nominatim(user_agent="geoapiExercises")

    location = geolocator.reverse(str(latitude) + "," + str(longitude))

    return str(location)
