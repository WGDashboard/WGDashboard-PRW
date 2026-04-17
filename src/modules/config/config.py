#!/bin/env python3

import logging as log
import flask

from .config_utils import config_utils

class config():
    @staticmethod
    def filter(config_data: dict, filter_keyword: str) -> tuple[bool, dict]:
        """
        Helper function to grab a specific part of the config
        """
        lower_filter_keyword = filter_keyword.lower()

        for section_name, section_values in config_data.items():
            if str(section_name).lower() == lower_filter_keyword:
                if isinstance(section_values, dict):
                    return True, dict(section_values)

        log.error("failed to properly filter the config")
        return False, {}

    @staticmethod
    def read() -> tuple[bool, dict]:
        """
        check some basic things and then return the dict containing the config data
        """

        ok, candidate_path = config_utils.search_known_paths()
        if not ok:
            log.error("failed to retrieve a valid path for the config")
            return False, {}

        ok, config_data = config_utils.read_data(candidate_path)
        if not ok:
            log.error("failed to read data from filepath")
            return False, {}

        return True, config_data

    @staticmethod
    def update(target_section: str, target_key: str, new_value) -> bool:
        lower_target_section = target_section.lower()
        lower_target_key = target_key.lower()

        ok, config_data = config.read()
        if not ok:
            log.error("failed to read the config successfully")
            return False
        
        if not config_utils.find_section(config_data, lower_target_section):
            log.error("failed to find the given section")
            return False
        if not config_utils.find_key(config_data, lower_target_section, lower_target_key):
            log.error("failed to find the given key in the given section")
            return False

        ok = config_utils.write_key(config_data, lower_target_section, lower_target_key, new_value)
        if not ok:
            log.error("failed to write the key to the file")
            return False

        return True