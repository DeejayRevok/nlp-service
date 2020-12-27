FROM python:3.8-buster
COPY ./ /app/nlp_service

WORKDIR /app

RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
RUN apt-get install apt-transport-https -y
RUN echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-7.x.list
RUN apt-get update && apt-get install metricbeat

RUN pip install --upgrade pip
RUN pip install -r ./nlp_service/requirements.txt

RUN python -m spacy download 'es_core_news_sm'

COPY ./tools_config/metricbeat.yml /etc/metricbeat/metricbeat.yml

EXPOSE 8082
CMD service metricbeat start && export PYTHONPATH=${PYTHONPATH}:/app/nlp_service && python ./nlp_service/webapp/main.py -p DOCKER