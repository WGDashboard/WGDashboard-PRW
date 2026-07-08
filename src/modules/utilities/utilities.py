#!/bin/env python3

import logging as log

import json
import os
import urllib.request

from packaging import version

class utilities():
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
            log.error('failed to create directory')
            return False
    
    @staticmethod
    def update_info(running_version: str) -> tuple[bool, bool, str]:
        request = urllib.request.urlopen("https://api.github.com/repos/WGDashboard/WGDashboard/releases/latest", timeout=5).read()

        data = json.loads(request)
        latest_version = data.get('tag_name')
        latest_version_link = data.get('html_url')

        try:
            if version.parse(latest_version) > version.parse(running_version):
                log.info('there is an update available for this instance')
                return True, True, latest_version_link
            else:
                log.info('this instance is running the latest version')
                return True, False, latest_version_link
        except:
            return False, False, ''

    @staticmethod
    def ProtocolsEnabled() -> list[str]:
        from shutil import which
        protocols = []
        if which('awg') is not None and which('awg-quick') is not None:
            protocols.append("awg")
        if which('wg') is not None and which('wg-quick') is not None:
            protocols.append("wg")
        return protocols