FROM jupyter/datascience-notebook

ENV jupyter_home /home/jovyan

COPY requirements.txt  /usr/lib/requirements.txt
COPY secrets /usr/lib/secrets
RUN pip install -r /usr/lib/requirements.txt
RUN python -m spacy download en
ARG container_src_path
RUN echo $container_src_path
ENV PYTHONPATH="$container_src_path:${PYTHONPATH}"
USER root
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
RUN echo "deb http://repo.mongodb.org/apt/debian jessie/mongodb-org/3.6 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
RUN apt-get update
RUN apt-get install -y mongodb-org
USER $NB_USER
RUN pip install git+https://github.com/nesdis/djongo
ENV AIRFLOW_HOME /home/jovyan/src/etl/jobs
ENTRYPOINT bash