#!/usr/bin/python3

import logging
import os
import subprocess

_logger = logging.getLogger(__name__)

RESOURCES = os.environ.get("RESOURCES")
CUSTOM_REQUIREMENTS = os.environ.get("CUSTOM_REQUIREMENTS")

if CUSTOM_REQUIREMENTS:
    _logger.info("Installing custom pip requirements...")
    # Save custom entrypoint to local file
    custom_file = os.path.join(RESOURCES, "xxx-custom-pip-requirements.txt")
    with open(custom_file, "w+") as file:
        file.write(CUSTOM_REQUIREMENTS)
    # Execute custom entrypoint
    subprocess.check_call(
        [
            "pip",
            "install",
            "--user",
            "--no-cache-dir",
            "-r",
            custom_file,
        ]
    )
    # Cleanup
    os.remove(custom_file)
