import pandas as pd
import json
import gzip

import ir_datasets
from tqdm import tqdm
docsstore = ir_datasets.load("trec-tot/2023").docs_store()

def all_queries(qid, dataset):
    ret = []
    for i in ['1', '2', '3', '4']:
        queries = open(f'to-fuse/webis-red-0{i}/{dataset}/queries.jsonl', 'r').read()
        queries = [json.loads(i) for i in queries.split('\n') if i]
        queries = {str(i['qid']): i for i in queries}
        ret += [(qid + '_' + i, queries[qid]['query'])]
        if i == '4':
            ret += [(qid + '_orig', queries[qid]['query_0'])]
    
    return ret

for d in ['tot-train', 'tot-test', 'tot-dev']:
    run = pd.read_csv(f'to-fuse/webis-fus-01/{d}/run.txt', sep="\s+", names=["query", "q0", "docid", "rank", "score", "system"])
    run['query'] = run['query'].astype(str)

    with gzip.open(f'{d}-rerank.jsonl.gz', 'wt') as f:
        for qid in tqdm(run['query'].unique(), d):
            for new_qid, new_query in all_queries(qid, d):
                doc_ids = run[run['query'] == qid]['docid'].unique()
                pos = 1
                for docno in doc_ids:
                    f.write(json.dumps({"qid": new_qid, "query": new_query, "docno": str(docno), "text": docsstore.get(str(docno)).default_text()[:2500], "rank": pos, "score": 10000-pos}) + '\n')
                    pos += 1
