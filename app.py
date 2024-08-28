from flask import Flask, render_template, request, jsonify
import googlemaps
import requests
import os

app = Flask(__name__)

# Load API keys from environment variables
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

gmaps = googlemaps.Client(key='AIzaSyCZhL9Os-umPMEW9fF7y5TYsZ-tthc1Q7U')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_route', methods=['POST'])
def get_route():
    start_location = request.form.get('start_location')
    end_location = request.form.get('end_location')

    # Get directions from Google Maps
    directions_result = gmaps.directions(start_location, end_location)

    if not directions_result:
        return jsonify({'error': 'No route found'}), 404

    # Extract polyline
    route = directions_result[0]
    polyline = route['overview_polyline']['points']

    # Get weather information along the route
    weather_data = get_weather_along_route(start_location, end_location)

    return jsonify({
        'polyline': polyline,
        'weather_data': weather_data
    })

def get_weather_along_route(start_location, end_location):
    # Example cities, replace with real route points
    route_cities = [
        'Mumbai', 'Pune', 'Goa'
    ]

    weather_data = []

    for city in route_cities:
        lat, lon = get_lat_lon(city)
        if lat and lon:
            weather_response = requests.get(
                f'http://api.openweathermap.org/data/2.5/weather',
                params={
                    'lat': lat,
                    'lon': lon,
                    'appid': WEATHER_API_KEY,
                    'units': 'metric'
                }
            )
            print(f'Weather response for {city}: {weather_response.json()}')  # Debug print
            weather = weather_response.json()
            weather_data.append({
                'city': city,
                'lat': lat,
                'lon': lon,
                'weather': weather['weather'][0]['description'],
                'temperature': weather['main']['temp']
            })

    return weather_data


def get_lat_lon(city):
    geocode_response = gmaps.geocode(city)
    print(f'Geocode response for {city}: {geocode_response}')  # Debug print
    if geocode_response:
        location = geocode_response[0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None





if __name__ == '__main__':
    app.run(debug=True)
