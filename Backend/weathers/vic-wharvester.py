import logging, json, requests, socket
from flask import current_app

def main():

    data= requests.get('http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json').json()
    current_app.logger.info(f'Harvested one weather observation')

    requests.post(url='http://router.fission/weathers/melb-olympic-park',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(data)
    )

    data_Geelong = requests.get('http://reg.bom.gov.au/fwo/IDV60901/IDV60901.94857.json').json()
    current_app.logger.info(f'Harvested Geelong weather observation')
    requests.post(url='http://router.fission/weathers/geelong',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(data_Geelong)
    )
    
    
    data_Avalon = requests.get('http://reg.bom.gov.au/fwo/IDV60901/IDV60901.94854.json').json()
    current_app.logger.info(f'Harvested Avalon weather observation')
    requests.post(url='http://router.fission/weathers/avalon',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(data_Avalon)
    )
    

    data_melb_airpot = requests.get('http://reg.bom.gov.au/fwo/IDV60901/IDV60901.94866.json', timeout=10).json()
    current_app.logger.info(f'Harvested Melbourne-Airport weather observation')
    requests.post(url='http://router.fission/weathers/melb-airport',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(data_melb_airpot)
    )

    




    return 'OK'
