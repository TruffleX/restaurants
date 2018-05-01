
export host_base_path ?= $(shell pwd)
export host_data_path="$(host_base_path)/data"
export host_src_path="$(host_base_path)/src"
export host_notebooks_path="$(host_base_path)/jupyter-notebooks"
export container_data_path=/home/jovyan/data
export container_src_path=/home/jovyan/src
export container_notebooks_path=/home/jovyan/jupyter-notebooks
export secrets_path=secrets

build:
	make secrets
	docker build --tag nlp --build-arg container_src_path=$(container_src_path) .

run:
	make secrets
	docker run -i -t -p 8889:8889 \
	--env-file $(secrets_path) \
	-v $(host_data_path):$(container_data_path) \
	-v $(host_src_path):$(container_src_path) \
	-v $(host_notebooks_path):$(container_notebooks_path) \
	nlp

jupyter:
	make secrets
	docker run -i -t -p 8889:8889 \
	--env-file $(secrets_path) \
	--entrypoint "jupyter" \
	-v $(host_data_path):$(container_data_path) \
	-v $(host_src_path):$(container_src_path) \
	-v $(host_notebooks_path):$(container_notebooks_path) \
	nlp \
	notebook --port 8889

update_db:
	make secrets
	docker run -i -t -p 8889:8889 \
	--env-file $(secrets_path) \
	--entrypoint "python" \
	-v $(host_data_path):$(container_data_path) \
	-v $(host_src_path):$(container_src_path) \
	-v $(host_notebooks_path):$(container_notebooks_path) \
	nlp \
	$(container_src_path)/scripts/update_rss.py

notebook:
	make jupyter

run-get-data:
	docker exec data/yelp/get_data.py

secrets:
	python src/scripts/make_secrets.py