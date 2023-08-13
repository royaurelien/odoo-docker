#!/usr/bin/python3

import logging
import os

_logger = logging.getLogger(__name__)

RESOURCES = os.environ.get("RESOURCES")
CUSTOM_CONFIG = os.environ.get("CUSTOM_CONFIG")

if CUSTOM_CONFIG:
    _logger.info("Adding entrypoint configuration:\n%s" % CUSTOM_CONFIG)
    config_file = os.path.join(RESOURCES, "conf.d", "999-entrypoint.conf")
    with open(config_file, "w+") as file:
        file.write(CUSTOM_CONFIG)