from elasticsearch import Elasticsearch
from elasticsearch import NotFoundError

import sys
import json

integration = sys.argv[1]

es = Elasticsearch('https://elastic:change_me@localhost:9200/', verify_certs=False)

igs = list()
try:
    res_ingest_logs = es.ingest.get_pipeline(id=f"logs-{integration}.*")
    igs.extend([{key: val} for key, val in res_ingest_logs.body.items()])
    print(f"{len(res_ingest_logs.body.items())} logs ingest pipelines found.")
except NotFoundError:
    print("No logs ingest pipelines found.")
try:
    res_ingest_metrics = es.ingest.get_pipeline(id=f"metrics-{integration}.*")
    igs.extend([{key: val} for key, val in res_ingest_metrics.body.items()])
    print(f"{len(res_ingest_metrics.body.items())} metrics ingest pipelines found.")
except NotFoundError:
    print("No metrics ingest pipelines found.")

with open("dev_tools_ingest.txt", "w") as outfile: 
    outfile.write(f"# After below commands, {len(igs)} pipeline(s) exist(s)\n")
    outfile.write("# To check:\n")
    outfile.write(f"GET _ingest/pipeline/*-{integration}.*?filter_path=*._meta.managed\n")
    for ig in igs:
        iname = next(iter(ig.keys()))
        outfile.write("\n")
        outfile.write(f"PUT _ingest/pipeline/{iname}\n")
        json.dump(ig[iname], outfile, indent=2)
        outfile.write("\n")
