import requests

def verify_location_yandex(lat, lng, api_key='7b0c7127-aa6a-470e-970b-3034cca2805f'):
    # Construct the URL for Yandex reverse geocoding
    url = f"https://geocode-maps.yandex.ru/1.x/"
    
    # Query parameters
    params = {
        "geocode": f"{lng},{lat}",  # Note: Yandex uses "longitude,latitude" format
        "format": "json",  # Response format
        "apikey": api_key,
        "lang": "uz_UZ"   # Your Yandex API key
    }
    
    # Send a GET request to the API
    response = requests.get(url, params=params)
    
    # Parse the JSON response
    if response.status_code == 200:
        data = response.json()
        try:
            # Extract the formatted address
            address = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]
            return address
        except (KeyError, IndexError):
            return "No address found for the given coordinates."
    else:
        return f"HTTP Error: {response.status_code}"