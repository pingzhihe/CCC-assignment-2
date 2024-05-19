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
        "size": 10000,
        "query": {
            "match_all": {}
        }
    }

    try:
        response_start_time = time.time()
        results = es.search(index="geo_twitter_data", body=search_data)
        logging.info(f"Search request duration: {time.time() - response_start_time}s")
        hits = results['hits']['hits']
        twitter_data = []

        for hit in hits:
            source = hit['_source']
            bbox = source.get('bbox', None)
            if bbox:
                # 通常，bbox 应该包含两个坐标：[最小经度, 最小纬度, 最大经度, 最大纬度]
                coordinates = bbox['coordinates'][0]
                if len(coordinates) > 0 and len(coordinates[0]) == 2:
                    # 提取边界框的经纬度
                    min_lon, min_lat = coordinates[0]
                    max_lon, max_lat = coordinates[2]  # 通常在对角线位置
                    # 计算中心点
                    centroid_lon = (min_lon + max_lon) / 2
                    centroid_lat = (min_lat + max_lat) / 2
                    geometry = {"type": "Point", "coordinates": [centroid_lon, centroid_lat]}
                else:
                    geometry = None
            else:
                geometry = None

            if geometry:
                twitter_data.append({
                    'tweet_id': source.get('id', 'N/A'),
                    'created_at': source.get('created_at', 'N/A'),
                    'lang': source.get('lang', 'N/A'),
                    'location': source.get('location', 'N/A'),
                    'sentiment': float(source.get('sentiment', 0)),
                    'geometry': geometry
                })

        # 构建 GeoJSON 数据
        if twitter_data:
            features = []
            for data in twitter_data:
                feature = {
                    "type": "Feature",
                    "geometry": data['geometry'],
                    "properties": {
                        "tweet_id": data['tweet_id'],
                        "created_at": data['created_at'],
                        "lang": data['lang'],
                        "location": data['location'],
                        "sentiment": data['sentiment']
                    }
                }
                features.append(feature)

            geojson_data = {
                "type": "FeatureCollection",
                "features": features
            }

            response = {
                'status_code': 200,
                'data': geojson_data
            }

            logging.info(f"Function completed in {time.time() - start_time}s")
            return json.dumps(response)
        else:
            logging.info("No valid Twitter data found.")
            return json.dumps({"status_code": 200, "data": "No valid Twitter data found."})

    except Exception as e:
        logging.error(f"Error: {e}")
        return json.dumps({
            'status_code': 500,
            'error': str(e)
        })
