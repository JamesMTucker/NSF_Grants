FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

RUN : \
    && apt-get update \
    && apt-get install -y wget gcc make parallel jq libwww-perl

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN : \
    && wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir root/.conda \
    && sh Miniconda3-latest-Linux-x86_64.sh -b \
    && rm Miniconda3-latest-Linux-x86_64.sh

RUN : \
    && conda create -y -n nsf python=3.11

copy . src/

RUN : \
    && /bin/bash -c "cd src \
    && source activate nsf \
    && pip install -r requirements.txt \
    && make"
