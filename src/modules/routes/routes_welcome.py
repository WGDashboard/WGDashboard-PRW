import logging as log

import bcrypt
import flask
import hashlib
import json
import pyotp
import os
import werkzeug
from datetime import datetime

from .response import make_resp_obj
from .routes_utils import routes_utils
from .locale import localeman

from ..database.functions import functions
from ..config.config import config

routes_welcome = flask.Blueprint("routes_welcome", __name__)

@routes_welcome.route('/api/Welcome_Finish', methods=["POST"])
def api_welcome_finish():
    ok, config_other = config.filter(flask.current_app.wgd_config, 'OTHER')
    if not ok:
        log.error("failed to filter the config in-memory")
        return make_resp_obj(False, 'Internal error', {}, 500)

    req_data = flask.request.get_json()
    if not req_data:
        return make_resp_obj(False, "Invalid request body", {}, 400)

    if len(req_data["username"]) == 0:
        return make_resp_obj(False, "Username cannot be empty", {}, 400)
    
    if len(req_data["newPassword"]) < 7:
        return make_resp_obj(False, "Password must be at least 8 characters", {}, 400)
    
    if not config.update('ACCOUNT', 'username', req_data["username"]):
        log.error("failed to update the key in the configuration file")
        return make_resp_obj(False, 'Internal error', {}, 500)

    hashed_password = bcrypt.hashpw(req_data["newPassword"].encode('utf-8'), bcrypt.gensalt())

    if not config.update('ACCOUNT', 'password', hashed_password.decode('utf-8')):
        log.error("failed to update the key in the configuration file")
        return make_resp_obj(False, 'Internal error', {}, 500)

    if not config.update('OTHER', 'welcome_session', False):
        log.error("failed to update the key in the configuration file")
        return make_resp_obj(False, 'Internal error', {}, 500)

    # Very important to also refresh the config in-memory
    ok, flask.current_app.wgd_config = config.read()
    if not ok:
        log.error("failed to refresh the in-memory configuration")
        return make_resp_obj(False, 'Internal error', {}, 500)

    return make_resp_obj()

@routes_welcome.route('/api/Welcome_GetTotpLink')
def api_welcome_get_totp():
    ok, config_account = config.filter(flask.current_app.wgd_config, 'ACCOUNT')
    if not ok:
        log.error("failed to filter the config in-memory")
        return make_resp_obj(False, 'Internal error', {}, 500)
    
    if "totp_verified" not in config_account or not config_account["totp_verified"]:
        totp_key = pyotp.random_base32()

        ok = config.update('ACCOUNT', 'totp_key', totp_key)
        if not ok:
            log.error("failed to update the key in the configuration file")
            return make_resp_obj(False, 'Internal error', {}, 500)
        
        # Very important to also refresh the config in-memory
        ok, flask.current_app.wgd_config = config.read()
        if not ok:
            log.error("failed to refresh the in-memory configuration")
            return make_resp_obj(False, 'Internal error', {}, 500)

        return make_resp_obj(True, '', pyotp.totp.TOTP(totp_key).provisioning_uri(issuer_name="WGDashboard Admin"))

    return make_resp_obj(False, 'Internal error', {}, 500)

@routes_welcome.route('/api/Welcome_VerifyTotpLink', methods=["POST"])
def api_welcome_verify_totp():
    ok, config_account = config.filter(flask.current_app.wgd_config, 'ACCOUNT')
    if not ok:
        log.error("failed to filter the config in-memory")
        return make_resp_obj(False, 'Internal error', {}, 500)
    
    req_data = flask.request.get_json()
    totp_code = pyotp.TOTP(config_account['totp_key'], interval=30).now()

    totp_match = totp_code == req_data['totp']
    if totp_match:
        ok = config.update('ACCOUNT', 'totp_verified', True)
        if not ok:
            log.error("failed to update the key in the configuration file")
            return make_resp_obj(False, 'Internal error', {}, 500)

        ok = config.update('ACCOUNT', 'enable_totp', True)
        if not ok:
            log.error("failed to update the key in the configuration file")
            return make_resp_obj(False, 'Internal error', {}, 500)

        # Very important to also refresh the config in-memory
        ok, flask.current_app.wgd_config = config.read()
        if not ok:
            log.error("failed to refresh the in-memory configuration")
            return make_resp_obj(False, 'Internal error', {}, 500)

    return make_resp_obj(totp_match)