#!/bin/env python3

import os
import json
import flask

from .response import make_resp_obj

from ..config.config import config

class localeman:
    def __init__(self):
        _, self.wgd_config = config.read()
        self.locale_path = flask.current_app.locale_path

        try:
            path = os.path.join(self.locale_path, "supported_locales.json")

            with open(path, "r", encoding="utf-8") as locale_path:
                self.active_languages = sorted(
                    json.load(locale_path),
                    key=lambda x: x.get("lang_name", "")
                )
        except Exception:
            self.active_languages = []

    def get_language(self):
        ok, server_config = config.filter(self.wgd_config, "SERVER")
        if not ok:
            log.error("failed to filter the config in-memory")
            return None

        lang = server_config.get("wgdashboard_language", "en")
        if lang.lower() == "en":
            return None

        path = os.path.join(self.locale_path, f"{lang}.json")
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as lang_file:
                return json.load(lang_file)
        return None

    def get_available_languages():
        available_languages_path = "./static/locales/supported_locales.json"

        with open(os.path.join(available_languages_path), "r") as f:
            language_data = json.load(f)

        available_languages = sorted(language_data, key=lambda x: x['lang_name'])

        return available_languages

    def update_language(self, lang_id) -> bool:
        path = os.path.join(self.locale_path, f"{lang_id}.json")

        if not os.path.isfile(path):
            lang_id = "en"

        config.update("SERVER", "wgdashboard_language", lang_id)
        # Very important to also refresh the config in-memory
        ok, flask.current_app.wgd_config = config.read()
        if not ok:
            log.error("failed to refresh the in-memory configuration")
            return make_resp_obj(False, 'Internal error', {}, 500)
        return self.get_language()