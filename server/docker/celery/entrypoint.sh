#!/bin/bash -e

# Avvia Beat in background
celery -A app_celery.celery beat --loglevel INFO --schedule "${FARM_DATA}/schedule" &

# Avvia Worker in primo piano (così mantiene vivo il container)
celery -A app_celery.celery worker --pool threads --loglevel INFO
