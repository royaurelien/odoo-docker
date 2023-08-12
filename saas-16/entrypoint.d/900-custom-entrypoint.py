#!/usr/bin/python3

import logging
import os
import stat
import subprocess

_logger = logging.getLogger(__name__)

RESOURCES = os.environ.get("RESOURCES")
CUSTOM_ENTRYPOINT = os.environ.get("CUSTOM_ENTRYPOINT")

if CUSTOM_ENTRYPOINT:
    _logger.info("Executing custom entrypoint...")
    # Save custom entrypoint to local file
    custom_entrypoint = os.path.join(RESOURCES, "xxx-custom-entrypoint")
    with open(custom_entrypoint, "w+") as file:
        file.write(CUSTOM_ENTRYPOINT)
    # Make file executable
    st = os.stat(custom_entrypoint)
    os.chmod(custom_entrypoint, st.st_mode | stat.S_IEXEC)
    # Execute custom entrypoint
    subprocess.check_call(custom_entrypoint, cwd="/home/odoo")
    # Cleanup
    os.remove(custom_entrypoint)
