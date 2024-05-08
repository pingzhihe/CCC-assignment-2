import json
import sys
import threading
import os
import Mastodon_havester_helper
import datetime
import requests
import time
token_map = {
    'aus.social':os.getenv('AUS_SOCIAL_TOKEN'),
    'mastodon.au':os.getenv("MASTODON_AU_TOKEN")
}



# if len(sys.argv) != 2:
#     print("Usage: python Mastodon_havester.py <output_path>")\

# output_path = sys.argv[1]

instance_url = 'https://aus.social'

# Initialize variables
all_posts = []
current_date = datetime.datetime.now()
one_day_ago = current_date - datetime.timedelta(days=1)
api_url = f'{instance_url}/api/v1/timelines/public'
headers = {'Authorization': f'Bearer {token_map["aus.social"]}'}
params = {'limit': 100} 

print("Start havesting")
# Fetch data iteratively until one year ago
while True:
    response = requests.get(api_url, headers=headers, params=params)
    time.sleep(2)
    # Process the response
    if response.status_code == 200:
        data = response.json()
        if data:
            all_posts.extend(data)
            # Get the ID of the oldest post in the current batch
            max_id = data[-1]['id']
            # If the timestamp of the oldest post is older than one year ago, stop fetching
            print(data[-1]['created_at'])
            if datetime.datetime.strptime(data[-1]['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ') < one_day_ago:
                break
            # Update the max_id for the next request
            params['max_id'] = max_id
        else:
            # No more posts available
            break
    elif response.status_code == 429:
        print("Too many request: Code 429")
        time.sleep(20)
        continue
    else:
        print(f'Error: {response.status_code}')
        break

# Process all_posts as needed
print(f'Total posts fetched: {len(all_posts)}')