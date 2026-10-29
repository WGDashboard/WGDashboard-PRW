#!/bin/env python3

import flask

from ..database.functions import functions

class routes_utils():
    @staticmethod
    def is_valid_api_key(api_key: str) -> bool:
        database_session = flask.current_app.extensions["wgd_db_session"]
        valid_keys, _ = functions.retrieve_api_keys(database_session)
        valid_key_strings = []

        for key in valid_keys:
            valid_key_strings.append(key["key"])

        return api_key in valid_key_strings

    @staticmethod
    def is_path_allowed(path: str, white_list: list[str], is_admin_session: bool) -> bool:
        # Allow if session has admin role
        if is_admin_session:
            return True
        # Check white list
        for allowed_path in white_list:
            if path == allowed_path:
                return True
            if (
                allowed_path != "/"
                and allowed_path.endswith("/")
                and path.startswith(allowed_path)
            ):
                return True
        return False