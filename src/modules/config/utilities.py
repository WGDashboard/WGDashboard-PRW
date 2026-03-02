#!/bin/env python3

import logging as log

import configparser as cp
import os

class preflight_checks():
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
            log.debug('searching predefined locations for the config file, takes first one.')

            for path in possible_config_locations:
                log.debug(f'testing path: {path}')

                if os.path.exists(path):
                    log.debug(f'found a file at: {path}')
                    return True, path
                else:
                    continue
            return False, ''

        except Exception as err:
            log.error(f'error occured while searching for the config file: {err}')
            return False, ''

    def verify_contents(config_path: str) -> tuple[bool, dict]:
        '''
        Check the existing config file for contents
        '''
        config = cp.ConfigParser()

        try:
            log.debug('looking through the given config file')

            config.read(config_path)

            if len(config.sections()) == 0:
                log.error('empty config, no sections')
                return False, {}
            
            for section in config.sections():
                log.debug(f'checking integrity of section: {section}')

                if len(config.items(section)) == 0:
                    log.error('empty section, no keys or values')
                    return False, {}

            return True, dict(config.items())

        except cp.ParsingError as err:
            log.error(f'error parsing the ini config file: {err}')
            return False, {}

        except Exception as err:
            log.error(f'error occured while looking through the config file: {err}')
            return False, {}