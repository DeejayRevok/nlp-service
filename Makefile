build_chart:
	cat VERSION | xargs -I {} helm package -u --version {} --app-version {} helm/nlp-service

run_kombu_event_consumer:
	nohup metricbeat -e -c /etc/metricbeat/metricbeat.yml &
	nohup filebeat -e -c /etc/filebeat/filebeat.yml &
	python app/kombu_event_consumer_runner.py -c $(CONSUMER_NAME)
