
'''

Here is the code for the function that harvests the weather data from the BOM API and sends it to the router function.
The main entry of function is main().
This function harvests the weather data for New Sales Wales from:
1. Sydney Olympic Park
2. Sydney Harbour
3. Sydney Airport
'''

# Team 8
# Name: Can Wang, Kaisheng Su, Mingtao Yang, Zhihe Ping
# Student number:1176867, 1241049, 1527052, 1238760

import logging, json, requests, socket
from flask import current_app


def main():
    
    data_sydney_olympic = requests.get('https://reg.bom.gov.au/fwo/IDN60901/IDN60901.95765.json').json()
    current_app.logger.info(f'Harvested Sydney Olympic Park observation')

    requests.post(url='http://router.fission/weathers/syd-olympic-park',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(data_sydney_olympic)
    )

    data_sydney_harbour = requests.get('https://reg.bom.gov.au/fwo/IDN60901/IDN60901.95766.json').json()
    current_app.logger.info(f'Harvested Sydney Harbour observation')

    requests.post(url='http://router.fission/weathers/syd-harbour',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(data_sydney_harbour)
    )

    data_sydney_airport = requests.get('https://reg.bom.gov.au/fwo/IDN60901/IDN60901.94767.json').json()
    current_app.logger.info(f'Harvested Sydney Airport observation')

    requests.post(url='http://router.fission/weathers/syd-airport',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(data_sydney_airport)
    )

    return "OK"