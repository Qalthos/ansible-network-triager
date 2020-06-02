import logging
import os
import sys
from datetime import datetime, timedelta
from email.headerregistry import Address
from typing import Dict, List, Tuple, TypedDict

import yaml

EmailConfig = TypedDict(
    "EmailConfig", {"email": str, "password": str}, total=False
)
Repository = TypedDict("Repository", {"name": str, "labels": List[str]})


class Config:
    repos: List[Tuple[str, Repository]]
    maintainers: List[Address]
    sender: EmailConfig

    last_triage_date: datetime

    def __init__(self, config_location: str):
        # select config.yaml from cwd
        if not config_location:
            logging.info("config file not specified, setting default")
            config_location = "./config.yaml"

        logging.info(f"attempting to read config file: {config_location}")

        try:
            with open(config_location, "r") as config_file:
                config = yaml.safe_load(config_file)
            logging.info("config file successfully loaded")
        except FileNotFoundError as e:
            logging.critical(e)
            sys.exit()

        logging.info("parsing information from config file")

        # Populate org and repos to triage
        self.repos = []
        logging.debug("parsing orgs and repositories from config file")
        for org in config["orgs"]:
            for repo in org["repos"]:
                self.repos.append((org["name"], repo))

        # Populate maintainers list
        logging.debug("parsing list of maintainers from config file")
        self.maintainers = [
            Address(item["name"], addr_spec=item["email"])
            for item in config.get("maintainers", [])
        ]

        # Set address to send triage emails from
        logging.debug("parsing triager email and password from config file")
        self.sender = {}
        if "triager" in config:
            try:
                self.sender = {
                    "email": config["triager"]["address"],
                    "password": config["triager"]["password"],
                }
            except KeyError as exc:
                logging.error(
                    f"triager config malformed, key {exc!s} not found"
                )
            except TypeError:
                logging.error(
                    "triager config malformed, should be a dictionary"
                )
        else:
            logging.debug("triager not found in config, will not send email")

        # Set last triage date
        logging.debug("setting last triage date")
        self.last_triage_date = datetime.utcnow() - timedelta(
            days=int(config["timedelta"])
        )

        logging.info("config file successfully parsed")

    @property
    def token(self) -> Dict[str, str]:
        logging.debug("fetching oauth token")
        if os.getenv("GH_TOKEN"):
            return {"Authorization": "token {0}".format(os.getenv("GH_TOKEN"))}
        return {}

    @property
    def is_email_ready(self) -> bool:
        return bool(self.sender and self.maintainers)
