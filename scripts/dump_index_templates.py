from elasticsearch import Elasticsearch

import json

es = Elasticsearch('https://elastic:change_me@localhost:9200/', verify_certs=False)

cts = list()
cts.extend(es.cluster.get_component_template(name='logs-haproxy.*@package')['component_templates'])
cts.extend(es.cluster.get_component_template(name='metrics-haproxy.*@package')['component_templates'])
print(f"{len(cts)} component templates found.")

tmpls = list()
tmpls.extend(es.indices.get_index_template(name='logs-haproxy.*')['index_templates'])
tmpls.extend(es.indices.get_index_template(name='metrics-haproxy.*')['index_templates'])
print(f"{len(tmpls)} index templates found.")

with open("dev_tools_index.txt", "w") as outfile: 
    outfile.write(f"# After below commands, {len(cts)} component template(s) + {len(tmpls)} index template(s) exist(s)\n")
    outfile.write("# To check:\n")
    outfile.write("GET _component_template/*-haproxy.*?filter_path=*.name\n")
    outfile.write("GET _index_template/*-haproxy.*?filter_path=*.name\n")
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
