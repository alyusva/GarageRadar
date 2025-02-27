# garajes/utils.py
from geopy.geocoders import Nominatim

def get_center_coordinates(address):
    """Obtiene las coordenadas (lat, lon) de una dirección usando Nominatim."""
    geolocator = Nominatim(user_agent="garage_finder")
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    else:
        raise Exception("No se pudo obtener la geolocalización de la dirección.")
