build_chart:
	cat VERSION | xargs -I {} helm package -u --version {} --app-version {} helm/nlp-service