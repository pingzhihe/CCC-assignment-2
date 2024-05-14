import logging
import json
import requests
from flask import current_app
from elasticsearch8 import Elasticsearch

def main():
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )

    response = requests.get('http://router.fission/weather', timeout=30)
    json_data = response.json()

    current_app.logger.info(f'Observations to add: {json_data}')

    for obs in json_data['observations']['data']:
        doc = {
            'stationid': obs['wmo'],
            'timestamp': obs['aifstime_utc'],
            'geo': {
                'lat': obs['lat'],
                'lon': obs['lon']
            },
            'name': obs['name'],
            'air_temp': obs['air_temp'],
            'rel_hum': obs['rel_hum']
        }

        res = client.index(
            index='observations',   
            id=f'{obs["wmo"]}-{obs["aifstime_utc"]}',
            body=doc
        )
        
        current_app.logger.info(f'Indexed observation {obs["wmo"]}-{obs["aifstime_utc"]}')

    return 'OK'