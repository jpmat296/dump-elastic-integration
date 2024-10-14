from elasticsearch import Elasticsearch

import json

es = Elasticsearch('https://elastic:change_me@localhost:9200/', verify_certs=False)

igs = es.ingest.get_pipeline(id='logs-netflow.*')
print(f"{len(igs.body.keys())} ingest pipelines found.")

with open("dev_tools_ingest.txt", "w") as outfile: 
    outfile.write("# After below commands, 4 pipelines exist")
    outfile.write("# To check:\n")
    outfile.write("GET _ingest/pipeline/*-infoblox_nios.*?filter_path=*.description\n")
    for ig in igs.body.keys():
        outfile.write("\n")
        outfile.write(f"PUT _ingest/pipeline/{ig}\n")
        json.dump(igs[ig], outfile, indent=2)
        outfile.write("\n")
