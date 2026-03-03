#!/bin/env python3

import flask
import json

def make_resp_obj(message: str = "", data: dict = {}, http_code: int = 200) -> flask.wrappers.Response:
    resp_json_data = json.dumps({
        'message': message,
        'data': data
    })
    
    response = flask.make_response(resp_json_data, http_code)
    response.mimetype = 'application/json'

    return response