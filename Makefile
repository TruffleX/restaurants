
export host_base_path ?= $(shell pwd)
export host_data_path="$(host_base_path)/data"
export host_src_path="$(host_base_path)/src"
export container_data_path=/home/jovyan/data
export container_src_path=/home/jovyan/src
export secrets_path=secrets

build:
	make secrets
	docker build --tag nlp --build-arg container_src_path=$(container_src_path) .

run:
	docker run -i -t -p 8889:8889 --env-file $(secrets_path) -v $(host_data_path):$(container_data_path) -v $(host_src_path):$(container_src_path) nlp

run-get-data:
	docker exec data/yelp/get_data.py

secrets:
	python src/make_secrets.py