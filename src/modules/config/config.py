#!/bin/env python3

import logging as log

from .utilities import config_utilities

class config():
    @staticmethod
    def filter(config_contents: dict, filter_keyword: str) -> tuple[bool, dict]:
        '''
        Helper function to grab a specific part of the config
        '''
        for section_name, section_values in config_contents.items():
            if str(section_name).lower() == filter_keyword.lower():
                if isinstance(section_values, dict):
                    return True, dict(section_values)
        return False, {}

    @staticmethod
    def read() -> tuple[bool, dict]:
        '''
        check some basic things and then return the dict containing the config data
        '''

        ok, candidate_path = config_utilities.search_known_paths()
        if not ok:
            return False, {}
        ok, config_contents = config_utilities.verify_contents(candidate_path)
        if not ok:
            return False, {}

        return True, config_contents
    
    @staticmethod
    def update(section: str, key: str, value: str) -> bool:
        print(config_utilities.search_known_paths())
        print(section, key, value)
        return True
