import requests
import json
from datetime import datetime, timedelta,timezone
import time
from elasticsearch8 import Elasticsearch
def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()

def main():
    client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs= False,
        ssl_show_warn= False,
        basic_auth=(config('ES_USERNAME'), config('ES_PASSWORD'))
    )
    # API endpoint
    endpoint = 'https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites/{siteID}/parameters'

    now = datetime.now(timezone.utc)
    since = now - timedelta(hours=48)  
    until = now 
    since_str = since.strftime("%Y-%m-%dT%H:%M:%SZ")
    until_str = until.strftime("%Y-%m-%dT%H:%M:%SZ")
    site_ids = []
    extracted_data = []
    # Request headers with API key
    headers = {
        'Cache-Control': 'no-cache',
        'X-API-Key': config('EPA_API_KEY'),
        'User-Agent': config('USER_AGENT')
    }

    # Get all site id
    response = requests.get('http://router.fission/EPA/sites')
    # Check if request was successful
    if response.status_code == 200:
        # Parse response JSON
        sites = response.json().get("sites_info")
        print("All sites is get")
    else:
        # message = {
        #     'status_code': response.status_code,
        #     'error': "Failed to retrieve air monitoring sites."
        # }
        # return json.dumps(message)
        return "get_sites_fail"

    for entry in sites:
        site_id = entry.get('siteID')
        if site_id:
            site_ids.append(site_id)
    try:
        for site_id in site_ids:
            # print("fetching: ",site_id)
            url = endpoint.format(siteID=site_id)
            params = {
                'since':since_str,
                'until':until_str,
                'interval': "1HR_AV"
            }
            # Sending GET request
            response = requests.get(url, params=params, headers=headers)

            # Check if request was successful
            if response.status_code == 200:
                # Parse response JSON
                data = response.json()
                siteName = data['siteName']
                if data['geometry']['type']!='Point':
                    continue
                else:
                    position = data['geometry']['coordinates']
                
                if 'parameters' in data:
                    for parameter in data['parameters']:
                        bulk_data = []
                        parameterName = parameter['name']
                        readings = parameter['timeSeriesReadings'][0]["readings"]
                        for reading in readings:
                            insert_data = {
                                'siteID':site_id,
                                'siteName':siteName,
                                'geometry':{'lat': position[0], 'lon': position[1]},
                                'dataName': parameterName,
                                'since': reading.get('since'),
                                'until': reading.get('until'),
                                'averageValue': reading.get('averageValue'),
                                "unit": reading.get('unit'),
                            }
                            bulk_data.append({'index': {'_index': 'air-qualities'}})
                            bulk_data.append(insert_data)
                            # res = client.index(
                            #     index='air-qualities',
                            #     body= insert_data
                            # )
                            # extracted_data.append(insert_data)
                        bulk_json = '\n'.join(json.dumps(item) for item in bulk_data) + '\n'
                        response = client.bulk(body=bulk_json)
                        if response['errors']:
                            print("bulk error: ", response['errors']) 
                            return "Add fail"
                    # time.sleep(0.2)
                else:
                    print("Warning: 'parameters' key not found in response for siteID:", site_id)
            elif response.status_code == 404:
                print("Site does not exist for siteID:", site_id)
                # time.sleep(0.2)
                continue
            else:
                # message = {
                #     'status_code':response.status_code,
                #     'error_message':response.text
                # }
                # return json.dumps(message)
                return "fail"
            
        # return_data = {
        #     'status_code':200,
        #     'extracted_data': extracted_data
        # }
        # return json.dumps(return_data)
        return 'ok' 
    except Exception as e:
        print("status:500, message: ", str(e))
        return "fail"
