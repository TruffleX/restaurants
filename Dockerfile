FROM jupyter/datascience-notebook

ENV jupyter_home /home/jovyan

COPY src/requirements.txt  /usr/lib/requirements.txt
COPY secrets /usr/lib/secrets
RUN pip install -r /usr/lib/requirements.txt
RUN python -m spacy download en

RUN export $(cat /usr/lib/secrets | xargs)

ENTRYPOINT bash