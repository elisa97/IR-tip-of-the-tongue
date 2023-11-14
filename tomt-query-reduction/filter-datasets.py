#!/usr/bin/env python3
import gzip
from tqdm import tqdm
ids_to_remove = set([i.strip() for i in open('ids-to-remove-from-reddit-tomt')])

print(f'Have {len(ids_to_remove)} ids to remove.')

def process_dataset(d):
    filtered = 0
    with gzip.open(d + '.jsonl.gz', r) as input_file, gzip.open(d + '-without-reddit-tomt-test.jsonl.gz', w) as output_file:
        for i in tqdm(input_file):
            i_parsed = json.loads(i)
            if i_parsed['url'].split('comments/')[1].split('/') in ids_to_remove:
                filtered += 1
                continue
            if i_parsed['id'] in ids_to_remove:
                filtered += 1
                continue
            output_file.write(i)
    print(f'Filtered {filtered} entries.')

for dataset in ['training-data-main-06-07-2023', 'training-data-title-06-07-2023']:
    process_dataset(dataset)

