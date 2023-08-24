FROM webis/tira-ir-datasets-starter:0.0.54

RUN pip3 uninstall -y ir_datasets \
	&& pip3 install --no-deps git+https://github.com/mam10eks/ir_datasets.git@add-test-dataset-for-TREC-tip-of-the-tongue

RUN python3 -c 'import ir_datasets; print(list(ir_datasets.load("trec-tot/2023/dev").queries_iter())[:10])'

RUN python3 -c 'import ir_datasets; print(ir_datasets.load("trec-tot/2023/dev").docs_store().get("330"))'

RUN python3 -c 'import ir_datasets; print(ir_datasets.load("trec-tot/2023/train").docs_store().get("330"))'

RUN python3 -c 'import ir_datasets; print(ir_datasets.load("trec-tot/2023").docs_store().get("330"))'

RUN python3 -c 'import ir_datasets; print(list(ir_datasets.load("trec-tot/2023/train").queries_iter())[:10])'

RUN python3 -c 'import ir_datasets; print(list(ir_datasets.load("trec-tot/2023/test").queries_iter())[:10])'

RUN python3 -c 'import ir_datasets; print(list(ir_datasets.load("trec-tot/2023/test").docs_store().get("330")))'

ENTRYPOINT [ "/irds_cli.sh" ]

