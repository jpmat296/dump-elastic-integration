from elasticsearch import Elasticsearch

import json

es = Elasticsearch('https://elastic:change_me@localhost:9200/', verify_certs=False)

tmpls = es.indices.get_index_template(name='logs-panw.panos')
print(f"{len(tmpls['index_templates'])} index templates found.")

cts = es.cluster.get_component_template(name='logs-panw.panos@package')
print(f"{len(cts['component_templates'])} component templates found.")

with open("dev_tools_index.txt", "w") as outfile: 
    outfile.write("# After below commands, 1 index template + 1 component template exist\n")
    outfile.write("# To check:\n")
    outfile.write("GET _index_template/*-panw.*?filter_path=*.name\n")
    outfile.write("GET _component_template/*-panw.*?filter_path=*.name\n")
    for tmpl in tmpls['index_templates']:
        outfile.write("\n")
        outfile.write(f"PUT _index_template/{tmpl['name']}\n")
        json.dump(tmpl, outfile, indent=2)
        outfile.write("\n")
    for ct in cts['component_templates']:
        outfile.write("\n")
        outfile.write(f"PUT _component_template/{ct['name']}\n")
        json.dump(ct, outfile, indent=2)
        outfile.write("\n")
