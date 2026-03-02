#!/bin/env python3

import logging as log

from .utilities import preflight_checks

class reader():
    def read_config() -> dict:
        '''
        check some basic things and then return the dict containing the config data
        '''

        ok, candidate_path = preflight_checks.search_known_paths()
        if not ok:
            return {}
        ok, config_contents = preflight_checks.verify_contents(candidate_path)
        if not ok:
            return {}

        return config_contents

    def refresh_config(config_contents: dict) -> dict:
        log.debug(f'refreshing config values')
        return reader.read_config()