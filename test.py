import requests

# Define your OpenCage API key
API_KEY = '5f1c2589b1644425b243e94268a79121'

# Define the location you want to geocode
location = "Hanover, Germany"

# Construct the API request URL
url = f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={API_KEY}"

# Make the API request
response = requests.get(url)

# Check for HTTP errors
if response.status_code == 200:
    # Parse JSON response
    data = response.json()
    print("Raw API Response:")
    print(data)
else:
    print(f"HTTP Error: {response.status_code}")
    print(response.json())
