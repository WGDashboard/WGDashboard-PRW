#!/bin/env python3

import logging as log

import flask
import json
import os
import werkzeug

from .response import make_resp_obj
from .utilities import helpers
from .locale import localeman

from ..database.functions import functions
from ..config.config import config

routes = flask.Blueprint("routes", __name__)

white_list = [
    "/", # we need to whitelist /
    "/client",
    "/static/",
    "/fileDownload",
    "/api/authenticate",
    "/api/locale",
    "getDashboardConfiguration",
    "getDashboardTheme",
    "getDashboardVersion",
    "sharePeer/get",
    "isTotpEnabled",
    "validateAuthentication",
    "favicon.ico",
]

@routes.before_request
def auth_required():
    if flask.request.method.lower() == "options":
        return make_resp_obj("", {"status": True}, 200)

    ok, config_server = config.filter(flask.current_app.wgd_config, 'SERVER')
    if not ok:
        return make_resp_obj("Internal error", {}, 500)

    auth_required_flag = config_server.get('auth_req', True)
    api_key_enabled = config_server.get("wgdashboard_apikey", False)

    if not auth_required_flag:
        return

    path = flask.request.path
    api_key = flask.request.headers.get("wgdashboard-apikey")

    if api_key and api_key_enabled:
        if helpers.is_valid_api_key(api_key):
            return
        else:
            return make_resp_obj("WGDashboard API-key does not exist or is invalid/expired", {}, 401)

    if flask.session.get("role") == "admin":
        return

    if helpers.is_path_allowed(path, white_list, flask.session):
        return

    return make_resp_obj("Unauthorized access", {}, 401)

@routes.route('/api/authenticate', methods=["POST"])
def api_authenticate():
    ok, config_server = config.filter(flask.current_app.wgd_config, 'SERVER')
    if not ok:
        return make_resp_obj("Internal error", {}, 500)

    auth_required_flag = config_server.get('auth_req', True)

    if not auth_required_flag:
        ok, config_other = config.filter(flask.current_app.wgd_config, 'OTHER')
        if not ok:
            return make_resp_obj("Internal error", {}, 500)

        return make_resp_obj(
            "Login successful, no authentication required",
            {"welcome_session": config_other.get("welcome_session", False)},
            200
        )

    data = flask.request.get_json()
    if not data:
        return make_resp_obj("Invalid request body", {}, 400)
    
    return make_resp_obj("Authentication required", {}, 401)

@routes.route('/', defaults={'path': ''})
@routes.route('/<path:path>')
def index_handler(path):
    static_folder = flask.current_app.static_folder
    try:
        safe_path = werkzeug.utils.safe_join(static_folder, path)
        if not safe_path or not os.path.exists(safe_path):
            raise Exception()
        rel_path = os.path.relpath(safe_path, static_folder)
        return flask.send_from_directory(flask.current_app.static_folder, rel_path)

    except Exception:
        print(f"ROUTE NOT INPLEMENTED: {path}")
        return flask.send_from_directory(flask.current_app.static_folder, "index.html")

@routes.route('/api/locale')
def api_locale_handler():
    locale_manager = localeman()
    locale_data = locale_manager.get_language()

    return make_resp_obj("", locale_data, 200)

@routes.route('/health', methods=["GET"])
@routes.route('/healthz', methods=["GET"])
def health_handler():
    return make_resp_obj(
        "Health Endpoint",
        {"status": "ok"},
        200
    )