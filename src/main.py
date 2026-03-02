#!/bin/env python3

import logging as log

from modules.config.reader import reader

if __name__ == '__main__':
    log.basicConfig(level=log.DEBUG)

    config_contents = reader.read_config()
    log.info(config_contents)
    input()
    config_contents = reader.refresh_config(config_contents)
    log.info(config_contents)