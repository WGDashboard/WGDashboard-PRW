#!/bin/env python3

from pathlib import Path

from modules.config.config import config


application_directory = Path(__file__).parent
config_loaded, config_data = config.read()
if not config_loaded:
    raise RuntimeError("failed to read the WGDashboard configuration")

server_config_found, server_config = config.filter(config_data, "SERVER")
if not server_config_found:
    raise RuntimeError("the SERVER configuration section is missing")

hostname = server_config.get("hostname", "0.0.0.0")
port = server_config.get("port", 10086)

chdir = str(application_directory)
bind = f"{hostname}:{port}"
workers = 1
wsgi_app = "main:create_app()"
errorlog = "log/error_gunicorn.log"
accesslog = "log/access_gunicorn.log"
capture_output = True
pidfile = "gunicorn.pid"
