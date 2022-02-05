FROM python:3.9

RUN apt-get update && apt-get install -y texlive-full
RUN rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN apt update
RUN apt-get -y update && apt-get install -y \
	graphviz