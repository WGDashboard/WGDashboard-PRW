#!/bin/env python3

import logging as log
from logging.config import dictConfig

import flask
import json
import os
import secrets

from modules.config.reader import reader
from modules.database.database import database

from modules.utilities.utilities import utilities as util
from modules.utilities.logger import setup_logger

from modules.routes.routes import routes

if __name__ == '__main__':
    # Read the config file (ini)
    ok, config_contents = reader.read_config()
    if not ok:
        exit(1)
    found, config_server = util.filter_config(config_contents, 'SERVER')

    # Configure the loglevel of WGDashboard
    wanted_loglevel = config_server.get('log_level', 'DEBUG').upper()
    setup_logger(wanted_loglevel)

    # Get the database configuration from thee config
    found, config_database = util.filter_config(config_contents, 'DATABASE')
    if not found:
        exit(1)

    # Make the engine and create the infrastructure
    ok, engine, session = database.create_session(config_database)
    ok = database.ensure_contents(engine)

    prefix = config_server.get('app_prefix', '')

    # Configure the Flask app
    app = flask.Flask("WGDashboard", template_folder=os.path.abspath("./static/dist/WGDashboardAdmin"))
    app.register_blueprint(routes, url_prefix=prefix)

    app.wgd_config = config_contents

    app.secret_key = secrets.token_urlsafe(64)
    app.config['SESSION_TYPE'] = 'filesystem'

    app.engine = engine
    app.db_session = session

    debug_enabled = config_server.get('debug_enabled', False)
    hostname = config_server.get('hostname', '0.0.0.0')
    port = config_server.get('port', '10086')
    app.run(
        debug=debug_enabled,
        host=hostname,
        port=port,
        use_reloader=False
    )