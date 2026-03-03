#!/bin/env python3

import flask

from ..database.functions import functions

class helpers():
    @staticmethod
    def is_valid_api_key(api_key: str) -> bool:
        valid_keys, _ = functions.retrieve_api_keys(flask.current_app.db_session)
        valid_key_strings = []

        for key in valid_keys:
            valid_key_strings.append(key["key"])

        return api_key in valid_key_strings

    @staticmethod
    def is_path_allowed(path: str, white_list: list[str], session_data: dict) -> bool:
        # Allow if session has admin role
        if session_data.get("role") == "admin" and "username" in session_data:
            return True
        # Check white list
        for p in white_list:
            if p in path:
                return True
        return False