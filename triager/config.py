import logging
import sys
from datetime import datetime, timedelta

import yaml


def load_config(cfg):
    # select config.yaml from cwd
    parsed_config = {}
    if not cfg:
        logging.info("config file not specified, setting default")
        cfg = "./config.yaml"

    logging.info("attempting to read config file: {0}".format(cfg))

    try:
        with open(cfg, "r") as config_file:
            config = yaml.safe_load(config_file)
        logging.info("config file successfully loaded")
    except FileNotFoundError as e:
        logging.critical(e)
        sys.exit()

    logging.info("parsing information from config file")

    # Populate org and repos to triage
    repos = []
    logging.debug("parsing orgs and repositories from config file")
    for org in config["orgs"]:
        for repo in org["repos"]:
            repos.append((org["name"], repo))

    parsed_config["repos"] = repos

    # Populate maintainers list
    logging.debug("parsing list of maintainers from config file")
    parsed_config["maintainers"] = config["maintainers"]

    # Set address to send triage emails from
    logging.debug("parsing triager email and password from config file")
    parsed_config["sender"] = {
        "email": config.get("triager", {}).get("address"),
        "password": config.get("triager", {}).get("password"),
    }

    # Set last triage date
    logging.debug("setting last triage date")
    parsed_config["last_triage_date"] = datetime.utcnow() - timedelta(
        days=int(config["timedelta"])
    )

    logging.info("config file successfully parsed")

    return parsed_config
