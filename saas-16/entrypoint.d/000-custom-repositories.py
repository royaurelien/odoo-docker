#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from subprocess import check_call

import logging

_logger = logging.getLogger(__name__)


def get_env_bool(key):
    return str(os.environ.get(key)).lower() in ["true", "1"]


# Recreate and run git-aggregator
SOURCES = os.environ.get("SOURCES")
RESOURCES = os.environ.get("RESOURCES")
CUSTOM_REPOSITORIES = os.environ.get("CUSTOM_REPOSITORIES")
CUSTOM_REPOSITORIES_SHOULD_RAISE = get_env_bool("CUSTOM_REPOSITORIES_SHOULD_RAISE")

# Deprecated
if not CUSTOM_REPOSITORIES:
    CUSTOM_REPOSITORIES = os.environ.get("REPOS_YAML")
    if CUSTOM_REPOSITORIES:
        _logger.warning(
            "IMPORTANT: REPOS_YAML has been deprecated. "
            "Use CUSTOM_REPOSITORIES instead."
        )

if CUSTOM_REPOSITORIES and SOURCES:
    content = CUSTOM_REPOSITORIES
    repos_file = os.path.join(RESOURCES, "custom-repositories.yml")
    with open(repos_file, "w+") as file:
        file.write(content)
    _logger.info("Aggregating custom repositories..")
    # _logger.warning(content)
    try:
        check_call(
            [
                "autoaggregate",
                "--config",
                repos_file,
                "--install",
                "--user",
                "--output",
                os.path.join(SOURCES, "repositories"),
            ]
        )
    except Exception as e:
        _logger.error(
            "IMPORTANT: Could not aggregate custom repositories: %s" % repr(e)
        )
        if CUSTOM_REPOSITORIES_SHOULD_RAISE:
            raise e
