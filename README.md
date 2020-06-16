# nlp-service
News service NLP microservices

![NLP Services](https://github.com/DeejayRevok/nlp-service/workflows/NLP%20Services/badge.svg)
[![codecov](https://codecov.io/gh/DeejayRevok/nlp-service/branch/develop/graph/badge.svg?token=Iy48oweqr3)](https://codecov.io/gh/DeejayRevok/nlp-service)

### Local running

Run the parent's repo dev docker compose.

#### NLP celery worker
Inside the application folder run:
```
export JWT_SECRET={JWT_TOKEN_SECRET}
export PYTHONPATH={FULL_PATH_TO_APPLICATION_FOLDER}
pip install -r requirements_celery.txt
python nlp_celery_worker/celery_app.py -p LOCAL
```
#### NLP flower service
Inside the application folder run:
```
export PYTHONPATH={FULL_PATH_TO_APPLICATION_FOLDER}
pip install -r requirements_flower.txt
python nlp_celery_worker/flower_app.py -p LOCAL
```

#### NLP service
Inside the application folder run:
```
export PYTHONPATH={FULL_PATH_TO_APPLICATION_FOLDER}
pip install -r requirements.txt
python webapp/main.py -p LOCAL
```

