from elasticsearch8 import Elasticsearch
import json

def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()

def main():
    try:
        es = Elasticsearch (
                'https://elasticsearch-master.elastic.svc.cluster.local:9200',
                request_timeout=60,
                verify_certs=False,
                ssl_show_warn=False,
                basic_auth=(config('ES_USERNAME'), config('ES_PASSWORD'))
            )

        query = {
            "size": 10000,
            "query": {
                "match_all": {}
            }
        }

        result = es.search(index="air-qualities", body=query)
        air_qualities = result['hits']['hits']

        air_quality_dict = {}

        for hit in air_qualities:
            source = hit['_source']
            site_id = source['siteID']
            since = source['since']
            
            if site_id not in air_quality_dict:
                air_quality_dict[site_id] = {}
            
            if since not in air_quality_dict[site_id]:
                air_quality_dict[site_id][since] = []

            air_quality_dict[site_id][since].append(source)

        response = {'status_code': 200, 'data':air_quality_dict}
        return json.dumps(response)

    except Exception as e:
        error_response = {'status_code': 500, 'error_message': str(e)}
        return json.dumps(error_response)
