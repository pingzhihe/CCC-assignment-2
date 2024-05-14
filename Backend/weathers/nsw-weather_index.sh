curl -XPUT -k 'https://127.0.0.1:9200/nsw-weather' \
   --user 'elastic:elastic' \
   --header 'Content-Type: application/json' \
   --data '{
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    },  
    "mappings": {
        "properties": {
            "stationid": {
                "type": "keyword"
            },
            "timestamp": {
                "type": "date"
            },
            "utc_time": {
                "type": "date"  
            },
            "geo": {
                "type": "geo_point"
            },
            "name": {
                "type": "text"
            },
            "air_temp": {
                "type": "float"
            },
            "rel_hum": {
                "type": "float"
            },
            "pm10": {
                "type": "float"
            },
            "pm2p5": {
                "type": "float"
            },
            "ozone": {
                "type": "float"
            },
            "weather": {
                "type": "text"
            }
        }
    }
}'  | jq '.'