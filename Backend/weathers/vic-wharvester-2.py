'''
Author：Zhihe Ping

Here is the code for the function that harvests the weather data from the BOM API and sends it to the router function.
The main entry of function is main().
This function harvests the weather data for Victoria Region from:
1. Sk Kilda Harbour
2. Point Cook
'''
import logging, json, requests, socket
from flask import current_app

def main():

    data_sk_tilda= requests.get('http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95864.json').json()
    current_app.logger.info(f'Harvested Sk Kilda Harbour weather observation')

    requests.post(url='http://router.fission/weathers/sk-kilda-harbour',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(data_sk_tilda)
    )

    data_point_cook = requests.get('https://reg.bom.gov.au/fwo/IDV60901/IDV60901.95941.json').json()
    current_app.logger.info(f'Harvested Point Cook weather observation')
    requests.post(url='http://router.fission/weathers/point-cook',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(data_point_cook)
    )
    
    

    return 'OK'
