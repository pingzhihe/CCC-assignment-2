import requests
import os
import json
from datetime import datetime, timedelta,timezone
import time
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
    'X-API-Key': 'api',
    'User-Agent': "useragent"
}


# Get all site id
with open('EPA_sites.json', 'r') as f:
    sites = json.load(f)

for entry in sites:
    site_id = entry.get('siteID')
    if site_id:
        site_ids.append(site_id)
    else:
        print("SiteID not found in entry:", entry)


for site_id in site_ids:
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
        else:
            print("Warning: 'parameters' key not found in response for siteID:", site_id)
        time.sleep(1)
    elif response.status_code == 404:
        print("Site does not exist for siteID:", site_id)
        time.sleep(1)
        continue
    else:
        print("Failed to retrieve air monitoring sites. Status code:", response.status_code)
        print("Error message:", response.text)
        exit(0)

with open('all_site_data.json', 'w') as f:
    json.dump(extracted_data, f, indent=4)

# curl -X GET "https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites/77062cb7-3e3b-4984-b6d0-03dda76177f2/parameters" -H "Cache-Control: no-cache" -H "X-API-Key: e40ad1e9725e45658b1f919b0d5ba7fe"

