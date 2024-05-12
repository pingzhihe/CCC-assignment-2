import requests
import json
from datetime import datetime, timedelta,timezone
import time
def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()

def main():
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
        message = {
            'status_code': response.status_code,
            'error': "Failed to retrieve air monitoring sites."
        }
        return json.dumps(message)

    for entry in sites:
        site_id = entry.get('siteID')
        if site_id:
            site_ids.append(site_id)

    for site_id in site_ids:
        print("fetching: ",site_id)
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

            if 'parameters' in data:
                site_data = {
                    'siteID': site_id,
                    'siteName': data['siteName'],
                    'geometry': data['geometry'],
                    'parameters': data['parameters']
                }
                extracted_data.append(site_data)
                time.sleep(0.2)
            else:
                print("Warning: 'parameters' key not found in response for siteID:", site_id)
        elif response.status_code == 404:
            print("Site does not exist for siteID:", site_id)
            time.sleep(0.2)
            continue
        else:
            message = {
                'status_code':response.status_code,
                'error_message':response.text
            }
            return json.dumps(message)

    return json.dumps(extracted_data)
