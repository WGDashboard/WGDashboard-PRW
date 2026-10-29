#!/bin/env python3

import logging as log

import json
import os
import shutil
import urllib.request

from json import JSONDecodeError
from urllib.error import URLError

from packaging.version import InvalidVersion, parse

class utilities():
    @staticmethod
    def ensure_directory(path: str) -> bool:
        '''
        Make the directory if it does not exist yet, return only true if the directory was missing and created.
        '''

        log.debug("ensuring directory exists: %s", path)
        if os.path.isdir(path):
            log.debug("directory already exists: %s", path)
            return True
        
        try:
            os.mkdir(path)
            log.debug("created directory: %s", path)
            return True

        except OSError:
            log.exception("failed to create directory: %s", path)
            return False
    
    @staticmethod
    def update_info(running_version: str) -> tuple[bool, bool, str]:
        log.debug("checking for a newer WGDashboard release")
        try:
            with urllib.request.urlopen(
                "https://api.github.com/repos/WGDashboard/WGDashboard/releases/latest",
                timeout=5,
            ) as response:
                release_data = json.loads(response.read())

            if not isinstance(release_data, dict):
                raise ValueError("release response must be a JSON object")

            latest_version = release_data.get("tag_name")
            latest_version_link = release_data.get("html_url")
            if not isinstance(latest_version, str) or not isinstance(latest_version_link, str):
                raise ValueError("release response is missing tag_name or html_url")

            if parse(latest_version) > parse(running_version):
                log.info('there is an update available for this instance')
                return True, True, latest_version_link
            log.info('this instance is running the latest version')
            return True, False, latest_version_link
        except (URLError, OSError, JSONDecodeError, InvalidVersion, UnicodeDecodeError, ValueError):
            log.exception("failed to check for a WGDashboard update")
            return False, False, ''

    @staticmethod
    def protocols_enabled() -> list[str]:
        log.debug("checking installed WireGuard protocols")
        protocols = []
        if shutil.which('awg') is not None and shutil.which('awg-quick') is not None:
            protocols.append("awg")
        if shutil.which('wg') is not None and shutil.which('wg-quick') is not None:
            protocols.append("wg")
        log.debug("enabled WireGuard protocols: %s", protocols)
        return protocols