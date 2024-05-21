'''
Here is the code for the function that harvests the weather data from the BOM API and sends it to the router function.
The main entry of function is main().
This function harvests the weather data for Victoria Region from:
1. Sk Kilda Harbour
2. Point Cook
'''
# Team 8
# Name: Can Wang, Kaisheng Su, Mingtao Yang, Zhihe Ping
# Student number:1176867, 1241049, 1527052, 1238760
import logging, json, requests, time
from flask import current_app

def fetch_data_with_retries(url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Check if the status code is 200
            return response.json()
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            current_app.logger.error(f'Error fetching data (attempt {attempt + 1}/{retries}): {e}')
            if attempt < retries - 1:
                time.sleep(delay)  # Wait for a while before retrying
            else:
                raise  # if all retries failed, re-raise the exception

def main():
    locations = {
        'sk-kilda-harbour': 'http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95864.json',
        'point-cook': 'https://reg.bom.gov.au/fwo/IDV60901/IDV60901.95941.json'
    }

    for location, url in locations.items():
        try:
            data = fetch_data_with_retries(url)
            current_app.logger.info(f'Harvested {location} weather observation') # Receive the data and send it to the router function
            requests.post(
                url=f'http://router.fission/weathers/{location}',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(data)
            )
        except Exception as e:
            current_app.logger.error(f'Failed to fetch and send data for {location} after retries: {e}')

    return 'OK'