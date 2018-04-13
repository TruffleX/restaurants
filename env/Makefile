
export host_env_path ?= $(shell pwd)
export host_base_path=$(shell dirname $(host_env_path))
export host_data_path="$(host_base_path)/data"
export container_data_path=/home/jovyan

build:
	docker build --tag nlp .

run:
	docker run -i -t -p 8889:8889 -v $(host_data_path):$(container_data_path) nlp

run-get-data:
	docker exec data/yelp/get_data.py