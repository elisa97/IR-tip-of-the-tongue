FROM webis/tira-ir-starter-chatnoir:0.0.3

COPY oracle-pipeline-chatnoir.ipynb  /workspace

RUN jupyter trust /workspace/*.ipynb \
	&& pip3 uninstall -y tira && pip3 install trectools tira==0.0.29

ENTRYPOINT ["jupyter-lab", "--allow-root", "--ip", "0.0.0.0"]
