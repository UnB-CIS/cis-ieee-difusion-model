FROM jupyter/scipy-notebook:latest

RUN pip install requests feature_engine

WORKDIR /home/caefleury/Documents/ieee-cis/cis-difusion-model/src

EXPOSE 8888
