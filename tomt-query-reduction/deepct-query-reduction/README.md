
```
tira-run \
	--image mam10eks/tomt-query-reduction-deepct:0.0.1 \
	--input-directory ${PWD}/../tot-dev \
	--output-directory ${PWD}/tot-dev-deepct-predictions \
	--command 'python3 /code/deepct_query_reduction.py --input_file $inputDataset/queries.jsonl --output_file $outputDir/predictions.json'
```

```
tira-run \
	--image mam10eks/tomt-query-reduction-deepct:0.0.1 \
	--input-directory ${PWD}/../tot-train \
	--output-directory ${PWD}/tot-train-deepct-predictions \
	--command 'python3 /code/deepct_query_reduction.py --input_file $inputDataset/queries.jsonl --output_file $outputDir/predictions.json'
```

```
tira-run \
	--image mam10eks/tomt-query-reduction-deepct:0.0.1 \
	--input-directory ${PWD}/../tot-test \
	--output-directory ${PWD}/tot-test-deepct-predictions \
	--command 'python3 /code/deepct_query_reduction.py --input_file $inputDataset/queries.jsonl --output_file $outputDir/predictions.json'
```

```
docker build -t mam10eks/tomt-query-reduction-deepct:0.0.1 .
```
