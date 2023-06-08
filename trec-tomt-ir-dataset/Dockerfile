FROM webis/tira-ir-datasets-starter:0.0.54

RUN pip3 uninstall -y ir_datasets \
	&& pip3 install --no-deps git+https://github.com/mam10eks/ir_datasets.git@trec-tip-of-the-tongue

RUN python3 -c 'import ir_datasets; print(list(ir_datasets.load("trec-tip-of-the-tongue/dev").queries_iter())[:10])'

RUN python3 -c 'import ir_datasets; print(ir_datasets.load("trec-tip-of-the-tongue/dev").docs_store().get("330"))'

RUN python3 -c 'import ir_datasets; print(ir_datasets.load("trec-tip-of-the-tongue/train").docs_store().get("330"))'

RUN python3 -c 'import ir_datasets; print(ir_datasets.load("trec-tip-of-the-tongue").docs_store().get("330"))'

RUN python3 -c 'import ir_datasets; print(list(ir_datasets.load("trec-tip-of-the-tongue/train").queries_iter())[:10])'

RUN pip3 uninstall -y ir_datasets \
	&& pip3 install --no-deps git+https://github.com/mam10eks/ir_datasets.git@trec-tip-of-the-tongue

ENTRYPOINT [ "/irds_cli.sh" ]

