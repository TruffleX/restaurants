FROM jupyter/datascience-notebook

ENV jupyter_home /home/jovyan

COPY requirements.txt  /usr/lib/requirements.txt
RUN pip install -r /usr/lib/requirements.txt
RUN python -m spacy download en

ENTRYPOINT bash