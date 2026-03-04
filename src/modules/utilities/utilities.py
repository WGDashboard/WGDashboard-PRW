#!/bin/env python3

import logging as log

import os

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
            log.critical('failed to create directory')
            return False