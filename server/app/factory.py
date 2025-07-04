import logging
import os

from celery import Celery
from flask import Flask
from flask_cors import CORS
from prometheus_client import make_wsgi_app
from prometheus_flask_exporter import PrometheusMetrics
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from datetime import timedelta

from api import api
from reloader import get_config



def create_app():
    app = Flask('s4d_farm')

    # Trigger singleton init
    app.config.update(get_config())

    app.logger.setLevel(logging.DEBUG)
    for handler in app.logger.handlers:
        handler.setLevel(logging.DEBUG)

    app.register_blueprint(api)

    CORS(app)
    PrometheusMetrics(app)

    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/api/metrics': make_wsgi_app(),
    })

    return app


def create_celery():
    broker = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/1')
    celery = Celery(
        'ad_farm',
        broker=broker,
        include=['tasks'],
    )
    period_seconds = int(os.environ.get('SUBMIT_PERIOD',5))
    period = timedelta(seconds=period_seconds)

    celery.conf.beat_schedule = {
        f'submit_flags': {
            'task': 'tasks.submit_flags_task',
            'schedule': period,
        },
    }
    return celery
