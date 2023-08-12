#!/usr/bin/python3

import logging
import os
from contextlib import closing
from string import Template

_logger = logging.getLogger(__name__)

try:
    # Python 2, where io.StringIO fails because it is unicode-only
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from configparser import RawConfigParser

    parser = RawConfigParser(strict=False)
except ImportError:
    # Python 2, where strict=True doesn't exist
    from ConfigParser import RawConfigParser

    parser = RawConfigParser()

ODOO_VERSION = os.environ.get("ODOO_VERSION")
TARGET_FILE = os.environ.get("ODOO_RC", os.environ.get("OPENERP_SERVER"))
CONFIG_DIR = os.path.join(os.environ.get("RESOURCES"), "conf.d")
CONFIG_FILES = []

# Read all configuraiton files found in those folders
_logger.info("Merging found configuration files in %s", TARGET_FILE)
for file in sorted(os.listdir(CONFIG_DIR)):
    parser.read(os.path.join(CONFIG_DIR, file))

# Write it to a memory string object
with closing(StringIO()) as resultfp:
    parser.write(resultfp)
    resultfp.seek(0)
    # Process line by line
    # We'll skip lines with errores
    result = []
    for line in resultfp:
        line = line.strip()
        try:
            # Try to expand variables
            line = Template(line).substitute(os.environ)
        except KeyError:
            # If error, simply ignore this line
            _logger.warning("Skipping config line: %s (missing env)" % (line))
            continue
        result.append(line)
    # Merge config file
    result = "\n".join(result)
    _logger.debug("Resulting configuration:\n%s", result)
    # Write it to destination
    with open(TARGET_FILE, "w") as targetfp:
        targetfp.write(result)
