from factory import create_celery
from log import setup_logging
from prometheus_client import start_http_server
import socket
import os

def is_port_free(port, host='0.0.0.0'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False


setup_logging('DEBUG')

celery = create_celery()

PORT = 5011

if is_port_free(PORT):
    print(f"Starting Prometheus server on port {PORT}")
    start_http_server(PORT)
else:
    print(f"Prometheus server not started: port {PORT} already in use")