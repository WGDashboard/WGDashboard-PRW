#!/bin/env python3

import logging as log

import configparser as cp
import os

class config_utils():
    @staticmethod
    def search_known_paths() -> tuple[bool, str]:
        """
        Look at predefined paths on the filesystem for a config file
        """

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
    def read_data(config_path) -> tuple[bool, dict]:
        config = cp.ConfigParser()

        try:
            config.read(config_path)

            if len(config.sections()) == 0:
                return False, {}

            config_dict = {}
            for section in config.sections():
                new_items = {}

                for key, value in config.items(section):
                    key = key.lower()
                    val = value.strip().lower()

                    if val == 'true':
                        value = True
                    elif val == 'false':
                        value = False

                    new_items[key] = value

                config_dict[section.lower()] = new_items
            
            return True, config_dict

        except cp.ParsingError as err:
            return False, {}

    @staticmethod
    def find_section(config_data: dict, target_section: str) -> bool:
        if target_section not in config_data:
            log.error("target section not in the config")
            return False

        return True
    
    @staticmethod
    def find_key(config_data: dict, target_section: str, target_key: str) -> bool:
        if target_key not in config_data[target_section]:
            log.error("target key not in the config")
            return False

        return True

    @staticmethod
    def write_key(config_data: dict, target_section: str, target_key: str, new_value: str) -> bool:
        config_data[target_section][target_key] = new_value

        config = cp.ConfigParser()

        for section, values in config_data.items():
            config[section] = {}
            for key, value in values.items():
                config[section][key] = str(value)
        
        try:
            ok, candidate_path = config_utils.search_known_paths()
            if not ok:
                log.error("failed to retrieve a valid path for the config")
                return False

            with open(candidate_path, "w") as f:
                config.write(f)

            return True

        except Exception as err:
            log.info("exception occured",err)
            return False