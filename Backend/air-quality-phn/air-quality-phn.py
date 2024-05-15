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
                verify_certs= False,
                ssl_show_warn= False,
                basic_auth=(config('ES_USERNAME'), config('ES_PASSWORD'))
            )

        query = {
        "size":100,
            "_source": ["_id","phn_name","phn_code","dths_rspt3"],
            "query": {
                "match_all": {}
            }
        }


        result = es.search(index="premature_mortality", body=query)
        docs = result['hits']['hits']
        features = {}
        for doc in docs:
            _id = doc['_id']
            death_ratio = doc['_source']['dths_rspt3']/100000
            phn_name = doc['_source']['phn_name']
            phn_code = doc['_source']['phn_code']
            features[_id] = {
                '_id': _id,
                'death_ratio':death_ratio,
                'phn_code': phn_code,
                'PHNName': phn_name
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
                                            "index": "premature_mortality",
                                            "id": id,
                                            "path": "geometry"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            # query = {
            #     "_source": False,
            #     "query": {
            #     "bool": {
            #         "must": [
            #             {
            #             "exists": {
            #                 "field": "geometry"
            #             }
            #             }
            #         ],
            #         "filter": {
            #             "geo_shape": {
            #                 "geometry": {
            #                     "indexed_shape": {
            #                     "index": "premature_mortality",
            #                     "id": id,
            #                     "path": "geometry"
            #                     }
            #                 }
            #             }
            #         }
            #     }
            # },
            # "aggs": {
            #     "dataName_avg": {
            #         "terms": {
            #             "field": "dataName"
            #         },
            #         "aggs": {
            #             "avg_value": {
            #                 "avg": {
            #                     "field": "averageValue"
            #                 }
            #             }
            #         }
            #     }
            # }
            # }

            result2 = es.search(index="air-qualities", body=query)
            aggs_data = result2['hits']['hits']
            for data in aggs_data:
                if data['_source']['averageValue']!=None:
                    aggregation_data.append({
                        '_id': id,
                        'dataName': data['_source']['dataName'],
                        'avgValue': data['_source']['averageValue']
                    })


        unique_data_names = set()
        for data in aggregation_data:
            unique_data_names.add(data['dataName'])

        for id in ids:
            for data_name in unique_data_names:
                values = []
                for data in aggregation_data:
                    if data['_id'] == id and data['dataName'] == data_name:
                        values.append(data['avgValue'])
                features[id][data_name] = values
                
        response = {
            'status_code': 200,
            'data': list(features.values())
        }
        return json.dumps(response)
    except Exception as e:
        error_response = {'status_code': 500, 'error_message': str(e)}
        return json.dumps(error_response)