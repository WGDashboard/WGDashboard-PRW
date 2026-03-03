#!/bin/env python3

import logging as log

import os

class utilities():
    @staticmethod
    def filter_config(config_contents: dict, filter_keyword: str) -> tuple[bool, dict]:
        '''
        Helper function to grab a specific part of the config
        '''
        for section_name, section_values in config_contents.items():
            if str(section_name).lower() == filter_keyword.lower():
                if isinstance(section_values, dict):
                    return True, dict(section_values)
        return False, {}

    @staticmethod
    def ensure_directory(path: str) -> bool:
        '''
        Make the directory if it does not exist yet, return only true if the directory was missing and created.
        '''

        if os.path.exists(path) and os.path.isdir(path):
            return True
        
        try:
            os.mkdir(path)
            return True

        except Exception as err:
            log.critical('failed to create directory')
            return False