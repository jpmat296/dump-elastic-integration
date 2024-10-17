import requests
import json

base_url = 'https://elastic:change_me@localhost:5601/'

res = requests.post(url=f"{base_url}api/saved_objects/_export", verify=False, json={
        'type': '*'
    }, headers={
        'Content-Type': 'application/json; Elastic-Api-Version=2023-10-31',
        'kbn-xsrf': 'string',
    }
)

tag = 0
search = 0
dashboards = 0
# Last line is summary. Ignore it.
with open("objects.ndjson", "w") as outfile:
    for line in res.text.splitlines()[:-1]:
        obj = json.loads(line)
        if 'cisco_ise' in obj['id']:
            outfile.write(line)
            outfile.write('\n')
            if obj['type'] == 'tag':
                tag += 1
            elif obj['type'] == 'dashboard':
                dashboards += 1
            elif obj['type'] == 'search':
                search += 1
            else:
                print(f"Unknown object type: {obj['type']}")

print("Saved objects exported in file objects.ndjson")
print(f"{tag} tags exported")
print(f"{search} searches exported")
print(f"{dashboards} dashboards exported")
