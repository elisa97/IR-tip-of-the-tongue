FROM mam10eks/tomt-query-reduction-deepct:0.0.1-dev

ADD *.py /code/

ADD test-data /code/test-data

RUN cd /code \
	&& pytest

