
'''
Author：Zhihe Ping

Here is the code for the function that harvests the weather data from the BOM API and sends it to the router function.
The main entry of function is main().
This function harvests the weather data from:
1. Melbourne olympic park
2. Geelong
3. Avalon
4. Melbourne airport
'''
import logging, json, requests, socket
from flask import current_app


def main():
    
    data= requests.get('https://reg.bom.gov.au/fwo/IDN60901/IDN60901.95765.json').json()
    current_app.logger.info(f'Harvested Sydney Olympic Park observation')

    requests.post(url='http://router.fission/weathers/syd-olympic-park',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(data)
    )

    return "OK"