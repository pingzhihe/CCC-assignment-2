from elasticsearch8 import Elasticsearch
import json
import logging
import time

# 配置日志记录
logging.basicConfig(level=logging.INFO)

def main():
    start_time = time.time()
    logging.info("Function start")

    es = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )

    search_data = {
        "size": 100,
        "_source": ["_id", "phn_name", "dth_suic96", "dth_suic99","geometry"],
        "query": {"match_all": {}}
    }

    try:
        response_start_time = time.time()
        results = es.search(index="premature_mortality_2011", body=search_data)
        logging.info(f"Search request duration: {time.time() - response_start_time}s")

        hits = results['hits']['hits']
        features = []

        for doc in hits:
            _id = doc['_id']
            source = doc['_source']
            count_suic = source.get('dth_suic96')
            ratio_suic = source.get('dth_suic99')
            phn_name = source.get('phn_name')
            geometry_data = source.get('geometry')
            

            if geometry_data:
                geometry = None
                if geometry_data['type'] == 'Point':
                    geometry = geometry_data
                elif geometry_data['type'] == 'Polygon':
                    geometry = geometry_data
                elif geometry_data['type'] == 'MultiPolygon':
                    geometry = geometry_data
                
                if geometry:
                    features.append({
                        '_id': _id,
                        'count_suic': count_suic,
                        'ratio_suic': ratio_suic,
                        'phn_name': phn_name,
                        'geometry': geometry
                    })

        response = {
            'status_code': 200,
            'data': features
        }

        logging.info(f"Function completed in {time.time() - start_time}s")
        return json.dumps(response)

    except Exception as e:
        logging.error(f"Error: {e}")
        return json.dumps({
            'status_code': 500,
            'error': str(e)
        })
