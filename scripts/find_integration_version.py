import sys
import requests
import json

integration = sys.argv[1]

base_url = 'https://elastic:change_me@localhost:5601/'

res = requests.get(url=f"{base_url}api/fleet/epm/packages/{integration}", verify=False,
    headers={
        'Content-Type': 'application/json; Elastic-Api-Version=2023-10-31',
        'kbn-xsrf': 'string',
    })

if 'item' not in res.json():
    print(f"No elastic integration found with id {integration}.")
    sys.exit(1)

print(res.json()['item']['version'])
sys.exit(0)
