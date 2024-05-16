from flask import current_app, request
from elasticsearch8 import Elasticsearch
from datetime import datetime

def main():
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )
    print(request)
    print("updated functin v1")
    json_data = request.json
    current_app.logger.info(f'Observations to add: {json_data}')

    for obs in json_data['observations']['data']:
        timestamp = datetime.strptime(obs['aifstime_utc'], '%Y%m%d%H%M%S')
        formatted_timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        doc = {
            
            'stationid': obs['wmo'],
            'timestamp': formatted_timestamp,
            'geo': {
                'lat': obs['lat'],
                'lon': obs['lon']
            },
            'name': obs['name'],
            'air_temp': obs['air_temp'],
            'rel_hum': obs['rel_hum']
        }

        res = client.index(
            index='syd-obs',   
            id=f'{obs["wmo"]}-{formatted_timestamp}',
            body=doc
        )
        current_app.logger.info(f'Indexed observation {obs["wmo"]}-{obs["aifstime_utc"]}')

    return 'OK'