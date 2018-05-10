
export host_base_path ?= $(shell pwd)
export host_data_path="$(host_base_path)/data"
export host_src_path="$(host_base_path)/src"
export host_notebooks_path="$(host_base_path)/jupyter-notebooks"
export container_data_path=/home/jovyan/data
export container_src_path=/home/jovyan/src
export container_notebooks_path=/home/jovyan/jupyter-notebooks
export secrets_path=secrets
export IMAGE=trufflex
export IMAGE_AWS=380559525413.dkr.ecr.us-east-1.amazonaws.com/trufflex
export AIRFLOW_HOME="$(pwd)/src/etl/jobs"

setup:
	pip install awscli --upgrade --user
	pip install "apache-airflow[webserver, sqlite]"
	airflow initdb
	echo "" >> ~/.bash_profile
	echo "export TRUFFLEX_PATH=$(shell pwd)" >> ~/.bash_profile
	export PATH=~/.local/bin:$$PATH
	echo "Enter your TruffleX AWS credentials"
	aws configure

airflow-webserver:
	airflow initdb
	airflow webserver

build:
	make secrets
	docker build --tag $(IMAGE) --build-arg container_src_path=$(container_src_path) .
	docker tag $(IMAGE):latest $(IMAGE_AWS):latest

run:
	make secrets
	docker run -i -t -p 8889:8889 -p 8000:8000 \
	--env-file $(secrets_path) \
	-v $(host_data_path):$(container_data_path) \
	-v $(host_src_path):$(container_src_path) \
	-v $(host_notebooks_path):$(container_notebooks_path) \
	-e GRANT_SUDO=yes \
	$(IMAGE)

jupyter:
	make secrets
	docker run -i -t -p 8889:8889 -p 8000:8000 \
	--env-file $(secrets_path) \
	--entrypoint "jupyter" \
	-v $(host_data_path):$(container_data_path) \
	-v $(host_src_path):$(container_src_path) \
	-v $(host_notebooks_path):$(container_notebooks_path) \
	$(IMAGE) \
	notebook --port 8889

update_db:
	make secrets
	docker run -i -t -p 8889:8889 -p 8000:8000 \
	--env-file $(secrets_path) \
	--entrypoint "python" \
	-v $(host_data_path):$(container_data_path) \
	-v $(host_src_path):$(container_src_path) \
	-v $(host_notebooks_path):$(container_notebooks_path) \
	$(IMAGE) \
	$(container_src_path)/etl/rss.py

yelp_ingest:
	make secrets
	docker run -i -t -p 8889:8889 -p 8000:8000 \
	--env-file $(secrets_path) \
	--entrypoint "python" \
	-v $(host_data_path):$(container_data_path) \
	-v $(host_src_path):$(container_src_path) \
	-v $(host_notebooks_path):$(container_notebooks_path) \
	$(IMAGE) \
	$(container_src_path)/etl/jobs/yelp_ingest_no_airflow.py

app-dev:
	make secrets
	docker run -i -t -p 8889:8889 -p 8000:8000 \
	--env-file $(secrets_path) \
	--entrypoint "flask" \
	-v $(host_data_path):$(container_data_path) \
	-v $(host_src_path):$(container_src_path) \
	-v $(host_notebooks_path):$(container_notebooks_path) \
	-e FLASK_APP='flaskr' \
	-e FLASK_ENV='development' \
	-w $(container_src_path)/apps/flask-app \
	$(IMAGE) \
	run --host 0.0.0.0 --port 8000

notebook:
	make jupyter

run-get-data:
	docker exec data/yelp/get_data.py

secrets:
	python src/scripts/make_secrets.py

push-image:
	docker push $(IMAGE_AWS):latest

pull-image:
	docker pull $(IMAGE_AWS):latest

login:
	aws ecr get-login --no-include-email --region us-east-1 | bash