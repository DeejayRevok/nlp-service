FROM python:3.10-slim
COPY ./ /app

WORKDIR /app

RUN apt-get update
RUN apt-get -y install gcc
RUN apt-get install wget -y
RUN apt-get install gnupg -y
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
RUN apt-get install apt-transport-https -y
RUN echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-7.x.list
RUN apt-get update
RUN apt-get install git -y
RUN apt-get install metricbeat=7.11.2
RUN apt-get install filebeat
RUN apt-get install make

RUN pip install --upgrade pip
RUN pip install -r ./requirements-prod.txt
RUN pip install -r ./requirements-dev.txt

RUN mkdir /var/log/nlp-service

COPY ./tools_config/filebeat.yml /etc/filebeat/filebeat.yml
COPY ./tools_config/metricbeat.yml /etc/metricbeat/metricbeat.yml

RUN python -m spacy download 'es_core_news_md'
RUN python -m spacy download 'en_core_web_md'
RUN python -m nltk.downloader 'vader_lexicon'

ENV PYTHONPATH=${PYTHONPATH}:/app/app:/app/src
