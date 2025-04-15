from elasticsearch import Elasticsearch
from elasticsearch import NotFoundError

import sys
import json

integration = sys.argv[1]

es = Elasticsearch('https://elastic:change_me@localhost:9200/', verify_certs=False)

cts = list()
try:
    logs_resp = es.cluster.get_component_template(name=f"logs-{integration}.*@package")
    cts.extend(logs_resp['component_templates'])
    print(f"{len(logs_resp['component_templates'])} logs component templates found.")
except NotFoundError:
    print("No logs component templates found.")
try:
    metrics_resp = es.cluster.get_component_template(name=f"metrics-{integration}.*@package")
    cts.extend(metrics_resp['component_templates'])
    print(f"{len(metrics_resp['component_templates'])} metrics component templates found.")
except NotFoundError:
    print("No metrics component templates found.")    

tmpls = list()
try:
    logs_resp2 = es.indices.get_index_template(name=f"logs-{integration}.*")
    tmpls.extend(logs_resp2['index_templates'])
    print(f"{len(logs_resp2['index_templates'])} logs index templates found.")
except NotFoundError:
    print("No logs index templates found.")
try:
    metrics_resp2 = es.indices.get_index_template(name=f"metrics-{integration}.*")
    tmpls.extend(metrics_resp2['index_templates'])
    print(f"{len(metrics_resp2['index_templates'])} metrics index templates found.")
except NotFoundError:
    print("No metrics index templates found.")

with open("dev_tools_index.txt", "w") as outfile: 
    outfile.write(f"# After below commands, {len(cts)} component template(s) + {len(tmpls)} index template(s) exist(s)\n")
    outfile.write("# To check:\n")
    outfile.write(f"GET _component_template/*-{integration}.*?filter_path=*.name\n")
    outfile.write(f"GET _index_template/*-{integration}.*?filter_path=*.name\n")
    for ct in cts:
        outfile.write("\n")
        outfile.write(f"PUT _component_template/{ct['name']}\n")
        json.dump(ct['component_template'], outfile, indent=2)
        outfile.write("\n")
    for tmpl in tmpls:
        outfile.write("\n")
        outfile.write(f"PUT _index_template/{tmpl['name']}\n")
        json.dump(tmpl['index_template'], outfile, indent=2)
        outfile.write("\n")
