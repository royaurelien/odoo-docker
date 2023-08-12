#!/usr/bin/python3

import logging
import os
from subprocess import check_call

_logger = logging.getLogger(__name__)


def get_env_bool(key):
    return str(os.environ.get(key)).lower() in ["true", "1"]


PGDATABASE = os.environ.get("PGDATABASE")
AUTO_UPDATE_MODULES = get_env_bool("AUTO_UPDATE_MODULES")
CLICK_ODOO_UPDATE_WATCHER_MAX_SECONDS = os.environ.get(
    "CLICK_ODOO_UPDATE_WATCHER_MAX_SECONDS", 60
)

# Backwards compatibility
if not AUTO_UPDATE_MODULES:
    AUTO_UPDATE_MODULES = get_env_bool("FIXDBS")
    if AUTO_UPDATE_MODULES:
        _logger.warning("FIXBDS is deprecated. Use AUTO_UPDATE_MODULES instead.")

# Auto update modules
if AUTO_UPDATE_MODULES and PGDATABASE:
    _logger.info("Auto-updating modules on database '%s'.." % PGDATABASE)
    check_call(
        [
            "click-odoo-update",
            "--if-exists",
            "--watcher-max-seconds",
            str(CLICK_ODOO_UPDATE_WATCHER_MAX_SECONDS),
        ]
    )
