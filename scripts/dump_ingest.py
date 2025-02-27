from elasticsearch import Elasticsearch

import json

es = Elasticsearch('https://elastic:change_me@localhost:9200/', verify_certs=False)

igs = list()
res_ingest = es.ingest.get_pipeline(id='metrics-haproxy.*')
igs.extend([{key: val} for key, val in res_ingest.body.items()])
res_ingest = es.ingest.get_pipeline(id='logs-haproxy.*')
igs.extend([{key: val} for key, val in res_ingest.body.items()])
print(f"{len(igs)} ingest pipelines found.")

with open("dev_tools_ingest.txt", "w") as outfile: 
    outfile.write(f"# After below commands, {len(igs)} pipeline(s) exist(s)\n")
    outfile.write("# To check:\n")
    outfile.write("GET _ingest/pipeline/*-haproxy.*?filter_path=**.description\n")
    for ig in igs:
        iname = next(iter(ig.keys()))
        outfile.write("\n")
        outfile.write(f"PUT _ingest/pipeline/{iname}\n")
        json.dump(ig[iname], outfile, indent=2)
        outfile.write("\n")
