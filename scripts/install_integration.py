import requests
import json

base_url = 'https://elastic:change_me@localhost:5601/'

res = requests.post(url=f"{base_url}api/fleet/epm/packages/netflow/2.19.1", verify=False,
    headers={
        'Content-Type': 'application/json; Elastic-Api-Version=2023-10-31',
        'kbn-xsrf': 'string',
    })

print(f"Integration netflow version 2.19.1 installed.")
print(f"{len(res.json()['items'])} items installed")
