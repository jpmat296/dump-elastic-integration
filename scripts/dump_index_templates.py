from elasticsearch import Elasticsearch

import json

es = Elasticsearch('https://elastic:change_me@localhost:9200/', verify_certs=False)

cts = es.cluster.get_component_template(name='logs-netflow.log@package')
print(f"{len(cts['component_templates'])} component templates found.")

tmpls = es.indices.get_index_template(name='logs-netflow.log')
print(f"{len(tmpls['index_templates'])} index templates found.")

with open("dev_tools_index.txt", "w") as outfile: 
    outfile.write("# After below commands, 1 component template  + 1 index template exist\n")
    outfile.write("# To check:\n")
    outfile.write("GET _component_template/*-netflow.*?filter_path=*.name\n")
    outfile.write("GET _index_template/*-netflow.*?filter_path=*.name\n")
    for ct in cts['component_templates']:
        outfile.write("\n")
        outfile.write(f"PUT _component_template/{ct['name']}\n")
        json.dump(ct['component_template'], outfile, indent=2)
        outfile.write("\n")
    for tmpl in tmpls['index_templates']:
        outfile.write("\n")
        outfile.write(f"PUT _index_template/{tmpl['name']}\n")
        json.dump(tmpl['index_template'], outfile, indent=2)
        outfile.write("\n")
