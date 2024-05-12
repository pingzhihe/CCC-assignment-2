import logging, json, requests, socket
from flask import current_app

def main():

    data= requests.get('http://reg.bom.gov.au/fwo/IDN60901/IDN60901.95765.json').json()
    current_app.logger.info(f'Harvested Sydney-Olympic-Park weather observation')

    requests.post(url='http://router.fission/weathers/syd-olympic-park',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(data)
    )
    return 'OK'
