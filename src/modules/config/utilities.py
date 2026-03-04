#!/bin/env python3

import logging as log

import configparser as cp
import os

class config_utilities():
    @staticmethod
    def search_known_paths() -> tuple[bool, str]:
        '''
        Look at predefined paths on the filesystem for a config file
        '''

        possible_config_locations = [
            "./config.ini",
            f"{os.getenv('HOME')}/.config/wgdashboard/config.ini",
            "/etc/wgdashboard/config.ini",
        ]

        try:
            for path in possible_config_locations:
                if os.path.exists(path):
                    return True, path
                else:
                    continue
            return False, ''

        except Exception as err:
            return False, ''

    @staticmethod
    def verify_contents(config_path: str) -> tuple[bool, dict]:
        '''
        Check the existing config file for contents
        '''
        config = cp.ConfigParser()

        try:
            config.read(config_path)

            if len(config.sections()) == 0:
                return False, {}
            
            for section in config.sections():
                if len(config.items(section)) == 0:
                    config.remove_section(section)

            config_dict = {}
            for section in config.sections():
                items = dict(config.items(section))

                for key, value in items.items():
                    if value.strip().lower() == 'true':
                        items[key] = True
                    elif value.strip().lower() == 'false':
                        items[key] = False
                    else:
                        items[key] = value

                config_dict[section] = items

            return True, config_dict

        except cp.ParsingError as err:
            return False, {}

        except Exception as err:
            return False, {}