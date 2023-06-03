#!/usr/bin/env python3
import sys
import subprocess
from tqdm import tqdm
import json
import os
import datetime
from os.path import exists

def clean_urls(urls):
    ret = []
    for url in urls:
        url = url.split(')')[0]
        url = url.split('(')[-1]
        ret.append(url)        
    return ret
        
assert ['https://www.reddit.com/r/woahdude/comments/66wqhv/true_cyan_color_illusion/'] == clean_urls(['https://www.reddit.com/r/woahdude/comments/66wqhv/true_cyan_color_illusion/'])
assert ['https://www.reddit.com/r/woahdude/comments/66wqhv/true_cyan_color_illusion/'] == clean_urls(['https://www.reddit.com/r/woahdude/comments/66wqhv/true_cyan_color_illusion/)'])
assert ['https://www.reddit.com/r/woahdude/comments/66wqhv/true_cyan_color_illusion/'] == clean_urls(['[text](https://www.reddit.com/r/woahdude/comments/66wqhv/true_cyan_color_illusion/)nochmehrtext'])

def get_htmls(entry):
    links = clean_urls(entry['links_on_answer_path'])

    ret = dict()
    for link in links:
        html_file = f"websites/{link.split('://')[-1]}"
        if exists(html_file):
            for suffix in ['','/index.html']:
                if os.path.isfile(html_file + suffix):
                    ret[link] = html_file + suffix
                    break
            if link not in ret:
                raise ValueError(f'Todo: {link}')

    return ret

def download_page(reddit_entry):
    if get_htmls(reddit_entry):
        return

    current_directory = os.getcwd()
    links = clean_urls(reddit_entry['links_on_answer_path'])
    timestamp = int(reddit_entry['solved_utc'])
    time = datetime.datetime.utcfromtimestamp(timestamp)
    time_start = (time - datetime.timedelta(days=365)).strftime("%Y%m%d%H%M%S")
    time_end = (time + datetime.timedelta(days=365)).strftime("%Y%m%d%H%M%S")
    for link in links:
        command = ["docker", "run", "-v", f"{current_directory}/websites:/websites",
                   "hartator/wayback-machine-downloader", "--exact-url", "--from",
                   time_start, "--to", time_end, "--maximum-snapshot", "2", link
                  ]

        subprocess.run(command, check=True)


if __name__ == '__main__':
    urls = [json.loads(l) for l in open(sys.argv[1])]
    
    for url in tqdm(urls, sys.argv[1]):
        download_page(url)

