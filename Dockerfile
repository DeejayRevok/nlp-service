FROM python:3.8-slim
COPY ./ /app/nlp_service

WORKDIR /app

RUN apt-get update
RUN apt-get -y install gcc
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install wget -y
RUN apt-get install gnupg -y
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
RUN apt-get install apt-transport-https -y
RUN echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-7.x.list
RUN apt-get update
RUN apt-get install git -y

RUN pip install --upgrade pip
RUN pip install -r ./nlp_service/requirements-prod.txt

COPY ./tools_config/metricbeat.yml /etc/metricbeat/metricbeat.yml

RUN python -m spacy download 'es_core_news_md'
RUN python -m spacy download 'en_core_web_md'

CMD service metricbeat start && export PYTHONPATH=${PYTHONPATH}:/app/nlp_service && python ./nlp_service/worker/main.py -c ./nlp_service/configs/config_docker.yml