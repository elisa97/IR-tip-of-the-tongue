# TOMT


## Corpus construction

Website topics: I removed questions that point to websites that dont exist anymore or websites that are not in the clueweb22

## Requirements

Please install `Docker`, `git`, `python3`, and `tira`.

- Please use official documentation/tutorials to install `docker`, `git` and `python3` on your machine.
- Please run `pip3 install tira` to install the TIRA client library on your machine.

## Build the Docker images

Please run:

```
make build-docker
```

## Methods

### Baseline: ChatNoir using the original title

Please run:

```
make run-title-baseline
```

### Oracle Baseline: ChatNoir using reciprocal rank fusion over 

Please run:

```
make run-oracle-baseline
```

The output (e.g., `head -3 output-oracle-baseline/run.txt`) should look like:

```
20 0 clueweb22-en0024-09-06042 1 0.04762704813108039 chatnoir-oracle-baseline
20 0 clueweb22-en0041-37-00460 2 0.046871392288155164 chatnoir-oracle-baseline
20 0 clueweb22-en0023-36-06642 3 0.04569460390355913 chatnoir-oracle-baseline
```

### Idea 1:

Let ChatGPT/alpaca generate keywords for the website I am looking for.

Prompt: "I want to build a website for X. Please write keywords that I should include so that the webpage can be easily found."


https://chat.web.webis.de/chat-ui

Example:
I want to build a website selling t-shirts bags posters with text of whole book. Please write keywords that I should include so that the webpage can be easily found.


### Idea 2:

The Tip-of-the-Tongue track has now a training and validation dataset.

Use HDCT/DeepCT to remove unimportant terms from the documents and queries.

- Extract reddit questions with links to web pages
- download linked pages with https://github.com/hartator/wayback-machine-downloader
- Train a BERT Model (we already have the corresponding training scripts) to remove terms that do not occur in the query /
  - Dedicated models for (1) the query, and (2) the document
  - Multiple dedicated models for different fields: title, url, full text of the document

# Evaluation results for the Title Baseline

```
tira-run \
    --input-directory ${PWD}/output-title-baseline \
    --image tomt-ir-dataset \
    --command 'ir_measures tomt $inputDataset/run.txt nDCG@10 MRR P@3 Recall@3'
```

This should output the following:

```
nDCG@10	0.0000
RR	0.0000
P@3	0.0000
R@3	0.0000
```

# Evaluation results for the Oracle Baseline

```
tira-run \
    --input-directory ${PWD}/output-oracle-baseline \
    --image tomt-ir-dataset \
    --command 'ir_measures tomt $inputDataset/run.txt nDCG@10 MRR P@3 Recall@3'
```

This should output the following:

```
nDCG@10	0.8474
RR	1.0000
P@3	0.8889
R@3	0.3452
```


# Additional Resources

- The [PyTerrier tutorial](https://github.com/terrier-org/ecir2021tutorial)
- The [PyTerrier documentation](https://pyterrier.readthedocs.io/en/latest/)
- The [TIRA quickstart](https://github.com/tira-io/ir-experiment-platform/tree/main/tira-ir-starters)


