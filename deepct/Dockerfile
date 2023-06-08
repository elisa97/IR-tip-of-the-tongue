FROM tensorflow/tensorflow:1.15.0-gpu-py3

RUN rm /etc/apt/sources.list.d/cuda.list \
	&& rm /etc/apt/sources.list.d/nvidia-ml.list \
	&& apt-get update \
	&& apt-get install -y git-lfs wget \
	&& mkdir /tmp/del \
	&& cd /tmp/del \
	&& git lfs install \
	&& wget https://storage.googleapis.com/bert_models/2020_02_20/all_bert_models.zip \
	&& unzip all_bert_models.zip \
	&& mkdir /bert_uncased_L-12_H-768_A-12/ \
	&& cd /bert_uncased_L-12_H-768_A-12/ \
	&& mv /tmp/del/uncased_L-12_H-768_A-12.zip . \
	&& unzip uncased_L-12_H-768_A-12.zip \
	&& rm uncased_L-12_H-768_A-12.zip \
	&& rm -Rf /tmp/del \
	&& git clone https://github.com/AdeDZY/DeepCT.git /deepct

ENV BERT_BASE_DIR="/bert_uncased_L-12_H-768_A-12/"

