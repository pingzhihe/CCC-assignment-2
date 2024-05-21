from flask import current_app, request
from elasticsearch8 import Elasticsearch
from datetime import datetime

def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()


def main():
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=(config('ES_USERNAME'), config('ES_PASSWORD'))
    )
    print(request)
    print("updated functin v1")
    json_data = request.json
    current_app.logger.info(f'Observations to add: {json_data}')

    for obs in json_data['observations']['data']:
        timestamp = datetime.strptime(obs['local_date_time_full'], '%Y%m%d%H%M%S')
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
            'apparent_t': obs['apparent_t'],
            'rel_hum': obs['rel_hum'],
            'rain_trace': obs['rain_trace'],
            'wind_dir': obs['wind_dir'],
            'wind_spd_kmh' : obs['wind_spd_kmh'],
            'weather': obs['weather']
        }

        res = client.index(
            index='nsw-weather',   
            id=f'{obs["wmo"]}-{formatted_timestamp}',
            body=doc
        )
        current_app.logger.info(f'Indexed observation {obs["wmo"]}-{obs["aifstime_utc"]}')

    return 'OK'
