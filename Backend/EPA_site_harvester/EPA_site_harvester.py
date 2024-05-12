import requests
import json
def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()

def main():
    # API endpoint
    endpoint = 'https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites'

    # Request headers with API key
    headers = {
        'Cache-Control': 'no-cache',
        'X-API-Key': config('EPA_API_KEY'),
        'User-Agent': config('USER_AGENT')
    }

    params = {
        'environmentalSegment': 'air'
    }

    # Sending GET request
    response = requests.get(endpoint, params=params, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        # Parse response JSON
        data = response.json()
        records = data['records']
        extracted_sites = []

        for record in records:
            site_id = record['siteID']
            site_name = record['siteName']
            geometry = record['geometry']

            site_data = {
                'siteID': site_id,
                'siteName': site_name,
                'geometry': geometry
            }
            extracted_sites.append(site_data)

        success_message = {
            'status_code':200,
            'sites_info':extracted_sites
        }

        return json.dumps(success_message)

    else:
        error_message = {
            'status_code':response.status_code,
            'error': "Failed to retrieve air monitoring sites.",
            'text': response.text
        }
        return json.dumps(error_message)
        


