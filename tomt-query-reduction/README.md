# TOMT Long Query Reduction

```
tira-run --image registry.webis.de/code-lib/public-images/trec-tot-ir-datasets:0.0.1 --output-directory ${PWD}/tot-train --command '/irds_cli.sh --ir_datasets_id  trec-tip-of-the-tongue/train --skip_documents true  --output_dataset_truth_path $outputDir'
```

```
tira-run --image registry.webis.de/code-lib/public-images/trec-tot-ir-datasets:0.0.1 --output-directory ${PWD}/tot-dev --command '/irds_cli.sh --ir_datasets_id  trec-tip-of-the-tongue/dev --skip_documents true  --output_dataset_truth_path $outputDir'
```

```
tira-run --image registry.webis.de/code-lib/public-images/trec-tot-ir-datasets:0.0.2 --output-directory ${PWD}/tot-test --command '/irds_cli.sh --ir_datasets_id  trec-tot/2023/test --skip_documents true --skip_qrels true --output_dataset_truth_path $outputDir'
```

```
tira-run --export-approach-output ir-benchmarks/ir-lab-jena-sose-2023/PyTerrier-Index --dataset-for-export-approach-output trec-tip-of-the-tongue-dev-20230607-training --output-dir pyterrier-index
```

