from elasticsearch8 import Elasticsearch
from datetime import datetime
import json
def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()

def main():
    try:
        es = Elasticsearch (
                'https://elasticsearch-master.elastic.svc.cluster.local:9200',
                request_timeout=60,
                verify_certs= False,
                ssl_show_warn= False,
                basic_auth=(config('ES_USERNAME'), config('ES_PASSWORD'))
            )


        query = {
        "size":100,
            "_source": ["phn_name","phn_code","dth_resp88"],
            "query": {
                "match_all": {}
            }
        }


        result = es.search(index="premature_mortality_2011", body=query)
        docs = result['hits']['hits']
        features = {}
        for doc in docs:
            _id = doc['_id']
            death_ratio = doc['_source']['dth_resp88']/100000
            phn_name = doc['_source']['phn_name']
            phn_code = doc['_source']['phn_code']
            features[_id] = {
                '_id': _id,
                'death_ratio':death_ratio,
                'phn_code': phn_code,
                'phn_name': phn_name
            }

        ids = list(features.keys())
        
        aggregation_data = []
        for id in ids:
            print("searching: ", id)
            query = {
                "size": 10000,
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "exists": {
                                        "field": "geometry"
                                    }
                                }
                            ],
                            "filter": {
                                "geo_shape": {
                                    "geometry": {
                                        "indexed_shape": {
                                            "index": "premature_mortality_2011",
                                            "id": id,
                                            "path": "geometry"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

            result2 = es.search(index="air-qualities", body=query)
            aggs_data = result2['hits']['hits']
            for data in aggs_data:
                if data['_source']['averageValue']!=None:
                    aggregation_data.append({
                        '_id': id,
                        'dataName': data['_source']['dataName'],
                        'avgValue': data['_source']['averageValue'],
                        'since': data['_source']['since']
                    })


        unique_data_names = set()
        unique_since = set()
        for data in aggregation_data:
            unique_data_names.add(data['dataName'])
            unique_since.add(data['since'])
        
        sorted_date_times = sorted(unique_since, key=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ'))
        for id in ids:
            for data_name in unique_data_names:
                values = []
                for since in sorted_date_times:
                    values_since = []
                    for data in aggregation_data:
                        if data['_id'] == id and data['dataName'] == data_name and data['since']==since:
                            values_since.append(data['avgValue'])
                    if len(values_since)!=0:
                        values.append(sum(values_since)/len(values_since))
                    else:
                        values.append(None)
                features[id][data_name] = values
                
        response = {
            'status_code': 200,
            'data': list(features.values())
        }
        return json.dumps(response)
    except Exception as e:
        error_response = {'status_code': 500, 'error_message': str(e)}
        return json.dumps(error_response)