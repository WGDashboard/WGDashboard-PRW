#!/bin/env python3

import logging as log

import bcrypt
import flask
import hashlib
import json
import os
import werkzeug
from datetime import datetime

from .response import make_resp_obj
from .routes_utils import routes_utils
from .locale import localeman

from ..database.functions import functions
from ..config.config import config

from ..utilities.utilities import utilities
from ..utilities.statistics import statistics

routes = flask.Blueprint("routes", __name__)

white_list = [
    "/",
    "/favicon.ico",
    "/client",
    "/static/",
    "/api/auth",
    "/api/auth/validate",
    "/api/dashboard/locale",
    "/api/dashboard/configuration",
    "/api/dashboard/theme",
    "/api/dashboard/version",
    "/api/dashboard/totp",
    "sharePeer/get",
]

@routes.before_request
def authentication_required():
    if flask.request.method.lower() == "options":
        return make_resp_obj(True, "", {"status": True}, 200)

    ok, config_server = config.filter(flask.current_app.wgd_config, 'SERVER')
    if not ok:
        log.error("failed to filter the config in-memory")
        return make_resp_obj(False, "Internal error", {}, 500)

    auth_required_flag = config_server.get('auth_req', True)
    api_key_enabled = config_server.get("wgdashboard_apikey", False)

    if not auth_required_flag:
        return

    path = flask.request.path
    api_key = flask.request.headers.get("wgdashboard-apikey")

    if api_key and api_key_enabled:
        if routes_utils.is_valid_api_key(api_key):
            return
        else:
            return make_resp_obj(False, "WGDashboard API-key does not exist or is invalid/expired", {}, 401)

    if flask.session.get("role") == "admin":
        return

    if routes_utils.is_path_allowed(path, white_list, flask.session):
        return

    return make_resp_obj(False, "Unauthorized access", {}, 401)

@routes.route('/', methods=["GET"])
def index_handler():
        return flask.render_template("index.html")

@routes.route('/api/auth', methods=["POST"])
def api_authenticate():
    ok, config_server = config.filter(flask.current_app.wgd_config, 'SERVER')
    if not ok:
        log.error("failed to filter the config in-memory")
        return make_resp_obj(False, "Internal error", {}, 500)

    auth_required_flag = config_server.get('authentication_required', True)

    # Authentication disabled
    if not auth_required_flag:
        ok, config_other = config.filter(flask.current_app.wgd_config, 'OTHER')
        if not ok:
            log.error("failed to filter the config in-memory")
            return make_resp_obj(False, "Internal error", {}, 500)

        welcome_session_enabled = config_other.get("welcome_session", False)
        return make_resp_obj(True, "Login successful, no authentication required", {"welcome_session": welcome_session_enabled}, 200)

    # API key authentication
    given_api_key = flask.request.headers.get("wgdashboard-apikey")
    api_key_enabled = config_server.get("wgdashboard_apikey", False)

    if given_api_key and api_key_enabled:
        if routes_utils.is_valid_api_key(given_api_key):
            authentication_token = hashlib.sha256(f"{given_api_key}{datetime.now()}".encode()).hexdigest()

            flask.session['role'] = 'admin'
            flask.session['username'] = authentication_token

            resp = make_resp_obj(True,"Login successful", {}, 200)
            resp.set_cookie("authToken", authentication_token)
            flask.session.permanent = True
            return resp
        else:
            return make_resp_obj(False, "API key invalid", {}, 401)

    # Load account config
    ok, config_account = config.filter(flask.current_app.wgd_config, 'ACCOUNT')
    if not ok:
        log.error("failed to filter the config in-memory")
        return make_resp_obj(False, "Internal error", {}, 500)

    req_data = flask.request.get_json()
    if not req_data:
        return make_resp_obj(False, "Invalid request body", {}, 400)

    username = req_data.get("username")
    password = req_data.get("password")
    totp_code = req_data.get("totp")

    #stored_user_objects = functions.retrieve_user_objects(flask.current_app.db_session)
    #print(stored_user_objects)

    stored_username = config_account.get("username")
    stored_password = config_account.get("password")
    totp_enabled = config_account.get("enable_totp", False)
    totp_key = config_account.get("totp_key")

    # Validate password
    valid = bcrypt.checkpw(
        password.encode("utf-8"),
        stored_password.encode("utf-8")
    )

    # Validate TOTP
    totp_valid = False
    if totp_enabled:
        totp_valid = pyotp.TOTP(totp_key).now() == totp_code

    if (
        valid
        and username == stored_username
        and ((totp_enabled and totp_valid) or not totp_enabled)
    ):
        # Generate a session token
        authentication_token = hashlib.sha256(f"{username}{datetime.now()}".encode()).hexdigest()

        flask.session['role'] = 'admin'
        flask.session['username'] = authentication_token
        flask.session.permanent = True

        # Log success via your helper if available
        log.info(f"Login success: {username} from {flask.request.remote_addr}")

        ok, config_other = config.filter(flask.current_app.wgd_config, 'OTHER')
        welcome_msg = config_other.get("welcome_session", "Welcome back!") if ok else "Welcome!"

        resp = make_resp_obj(True, {"status": True}, 200)
        resp.set_cookie("authToken", authentication_token, httponly=True, samesite='Lax')
        return resp

    # Log failure
    log.warning(f"Login failed: {username} from {flask.request.remote_addr}")
    
    error_msg = "Invalid username, password, or OTP." if totp_enabled else "Invalid username or password."
    return make_resp_obj(False, error_msg, {"status": False}, 401)

    if totp_enabled:
            return make_resp_obj(False, "Sorry, your username, password or OTP is incorrect.", {}, 401)
    else:
        return make_resp_obj(False, "Sorry, your username or password is incorrect.", {}, 401)

@routes.route('/api/auth/validate', methods=["GET"])
def api_validate_auth():
    ok, config_server = config.filter(flask.current_app.wgd_config, 'SERVER')
    if not ok:
        log.error("failed to filter the config in-memory")
        return make_resp_obj(False, 'Internal error', {}, 500)

    auth_required_flag = config_server.get('auth_req', True)
    token = flask.request.cookies.get("authToken")

    if auth_required_flag:
        if token is None or token == "" or flask.session.get("username") != token:
            return make_resp_obj(False, "Invalid authentication", {}, 200)
    return make_resp_obj()

@routes.route('/api/dashboard/locale', methods=["GET"])
def api_retrieve_locale():
    locale_manager = localeman()
    locale_data = locale_manager.get_language()

    return make_resp_obj(True, "", locale_data, 200)

@routes.route('/api/dashboard/locale', methods=["PATCH"])
def api_locale_update():
    req_data = flask.request.get_json()
    if "lang_id" not in req_data.keys():
        return make_resp_obj(False, "Please specify a language id: lang_id")

    language_id = req_data.get("lang_id")

    locale_manager = localeman
    ok = locale_manager.update_language(language_id)
    if not ok:
        return make_resp_obj(False, "Failed to update the language id")
    
    locale_data = locale_manager.get_language()
    return make_resp_obj(True, "", locale_data)

@routes.route('/api/dashboard/locale/available', methods=["GET"])
def api_retrieve_available_locales():
    locale_manager = localeman()


@routes.route('/api/dashboard/version', methods=["GET"])
def api_retrieve_version():
    ok, config_server = config.filter(flask.current_app.wgd_config, 'SERVER')
    if not ok:
        log.error("failed to filter the config in-memory")
        return make_resp_obj(False, 'Internal error', {}, 500)
    
    return make_resp_obj(True, "", config_server.get("version"))

@routes.route('/api/dashboard/theme', methods=["GET"])
def api_retrieve_theme():
    ok, config_server = config.filter(flask.current_app.wgd_config, 'SERVER')
    if not ok:
        log.error("failed to filter the config in-memory")
        return make_resp_obj(False, 'Internal error', {}, 500)

    return make_resp_obj(True, "", config_server.get("wgdashboard_theme"), 200)

@routes.route('/api/dashboard/updatestatus', methods=["GET"])
def api_retrieve_update_status():
    utilities.update_available()
    return make_resp_obj()

@routes.route('/api/dashboard/configuration', methods=["GET"])
def api_retrieve_config():
    return make_resp_obj(data=flask.current_app.wgd_config)

@routes.route('/api/dashboard/totp', methods=["GET"])
def api_totp_status():
    ok, config_account = config.filter(flask.current_app.wgd_config, 'ACCOUNT')
    if not ok:
        log.error("failed to filter the config in-memory")
        return make_resp_obj(False, 'Internal error', {}, 500)

    data = config_account.get('enable_totp') and config_account.get('totp_verified')
    
    return make_resp_obj(True, "", data, 200)

@routes.route('/api/dashboard/wireguard/interfaces', methods=["GET"])
def api_retrieve_wireguard_configurations():
    ok, config_server = config.filter(flask.current_app.wgd_config, 'SERVER')
    if not ok:
        log.error("failed to filter the config in-memory")
        return make_resp_obj(False, 'Internal error', {}, 500)

    if "wg_conf_path" not in config_server:
        return make_resp_obj(False, 'Internal error', {}, 500)

    wireguard_path = config_server.get('wg_conf_path', '/etc/wireguard')
    if os.path.exists(wireguard_path):
        present_confs = os.listdir(wireguard_path)
        present_confs.sort()

        log.info(present_confs)
    
    return make_resp_obj(True, 'Wireguard', {}, 200)

@routes.route('/api/dashboard/statistics', methods=["GET"])
def api_system_status():
    status = statistics()
    return make_resp_obj(True, "", status.to_json(), 200)

@routes.route('/health', methods=["GET"])
@routes.route('/healthz', methods=["GET"])
def health_handler():
    return make_resp_obj(True, "Health Endpoint", {"status": "ok"}, 200)