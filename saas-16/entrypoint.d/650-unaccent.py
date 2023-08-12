#!/usr/bin/python3

import logging
import os
from subprocess import check_call

_logger = logging.getLogger(__name__)


def get_env_bool(key):
    return str(os.environ.get(key)).lower() in ["true", "1"]


UNACCENT = get_env_bool("UNACCENT")
PGDATABASE = os.environ.get("PGDATABASE")

# Install unaccent
if UNACCENT and PGDATABASE:
    try:
        check_call(["psql", "-c", "CREATE EXTENSION IF NOT EXISTS unaccent;"])
    except Exception:
        pass
