build-docker:
	docker build -t registry.webis.de/code-lib/public-images/trec-tot-ir-datasets:0.0.1 trec-tomt-ir-dataset
	docker build -t registry.webis.de/code-lib/public-images/trec-tot-ir-resiliparse:0.0.1 -f baseline-title/Dockerfile.resiliparse baseline-title
	docker build -t registry.webis.de/code-lib/public-images/deepct:0.0.1 deepct
	docker build -t tomt-ir-dataset tomt-ir-dataset
	docker build -t tomt-baseline-oracle baseline-oracle
	docker build -t tomt-baseline-title baseline-title


deepct-shell:
	docker run --rm -ti -v ${PWD}:/data -w /deepct registry.webis.de/code-lib/public-images/deepct:0.0.1

tomt-dataset-tira/queries.jsonl:
	tira-run \
		--output-directory ${PWD}/tomt-dataset-tira \
		--image tomt-ir-dataset \
		--allow-network true \
		--command '/irds_cli.sh --ir_datasets_id tomt --output_dataset_path $outputDir'

run-title-baseline:
	tira-run \
		--input-directory $${PWD}/tomt-dataset-tira \
		--image tomt-baseline-title \
		--allow-network true \
		--output-directory $${PWD}/output-title-baseline \
		--command '/workspace/run-pyterrier-notebook.py --input $$inputDataset --output $$outputDir --notebook /workspace/title-pipeline-chatnoir.ipynb'

run-oracle-baseline:
	tira-run \
		--input-directory $${PWD}/tomt-dataset-tira \
		--image tomt-baseline-oracle \
		--allow-network true \
		--output-directory $${PWD}/output-oracle-baseline \
		--command '/workspace/run-pyterrier-notebook.py --input $$inputDataset --output $$outputDir --notebook /workspace/oracle-pipeline-chatnoir.ipynb'

jupyter: tomt-dataset-tira/queries.jsonl
	docker run -p 8888:8888 --rm -ti -v ${PWD}:/workspace tomt-baseline-title

crawl-urls-in-progress:
	./crawl-outlinks.py all-links-on-answer-paths/xaa

