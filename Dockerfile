FROM jupyter/datascience-notebook

ENV jupyter_home /home/jovyan

COPY src/requirements.txt  /usr/lib/requirements.txt
COPY secrets /usr/lib/secrets
RUN pip install -r /usr/lib/requirements.txt
RUN python -m spacy download en
ARG container_src_path
RUN echo $container_src_path
ENV PYTHONPATH="$container_src_path:${PYTHONPATH}"

ENTRYPOINT bash