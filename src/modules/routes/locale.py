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
            return None

        lang = server_config.get("wgdashboard_language", "en")
        if lang.lower() == "en":
            return None

        path = os.path.join(self.locale_path, f"{lang}.json")
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as lang_file:
                return json.load(lang_file)
        return None

#    def update_language(self, lang_id):
#        path = os.path.join(self.locale_path, f"{lang_id}.json")
#
#        if not os.path.isfile(path):
#            lang_id = "en"
#
#        util.set_config(self.wgd_config, "Server", "dashboard_language", lang_id)
#        return self.get_language()