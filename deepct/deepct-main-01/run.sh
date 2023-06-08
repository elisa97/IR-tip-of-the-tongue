#!/bin/bash

OUTPUT_DIR="${PWD}/output"

cd /deepct

python run_deepct.py \
	--task_name=marcodoc \
	--do_train=true \
	--do_eval=false \
	--do_predict=false \
	--data_dir=/data/deep-ct-main.jsonl \
	--vocab_file=${BERT_BASE_DIR}vocab.txt \
	--bert_config_file=${BERT_BASE_DIR}bert_config.json \
	--init_checkpoint=${BERT_BASE_DIR}bert_model.ckpt \
	--max_seq_length=128 \
	--train_batch_size=16 \
	--learning_rate=2e-5 \
	--num_train_epochs=3.0 \
	--recall_field=title \
	--output_dir=${OUTPUT_DIR}

