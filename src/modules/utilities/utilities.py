#!/bin/env python3

import logging as log

import os
import urllib.request

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
    def update_available() -> bool:
        request = urllib.request.urlopen("https://api.github.com/repos/WGDashboard/WGDashboard/releases/latest", timeout=5).read()

        data = json.loads(request)
        log.info(data)

    @staticmethod
    def ProtocolsEnabled() -> list[str]:
        from shutil import which
        protocols = []
        if which('awg') is not None and which('awg-quick') is not None:
            protocols.append("awg")
        if which('wg') is not None and which('wg-quick') is not None:
            protocols.append("wg")
        return protocols