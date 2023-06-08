FROM tensorflow/tensorflow:1.15.0-gpu-py3

RUN rm /etc/apt/sources.list.d/cuda.list \
	&& rm /etc/apt/sources.list.d/nvidia-ml.list \
	&& apt-get update \
	&& apt-get install -y git-lfs \
	&& mkdir /tmp/del \
	&& cd /tmp/del \
	&& git lfs install \
	&& git clone https://huggingface.co/google/bert_uncased_L-12_H-768_A-12 /bert_uncased_L-12_H-768_A-12 \
	&& git clone https://github.com/AdeDZY/DeepCT.git /deepct

ENV BERT_BASE_DIR="/bert_uncased_L-12_H-768_A-12/"

