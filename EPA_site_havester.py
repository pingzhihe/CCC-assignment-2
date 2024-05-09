import requests
import os
import json
# API endpoint
endpoint = 'https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites'

# Request headers with API key
headers = {
    'Cache-Control': 'no-cache',
    'X-API-Key': 'APIKEY',
    'User-Agent': "USER_AGENT"
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

    with open('extracted_sites.json', 'w') as f:
        json.dump(extracted_sites, f, indent=4)

else:
    print("Failed to retrieve air monitoring sites. Status code:", response.status_code)
    print("Error message:", response.text)
    


