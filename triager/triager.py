import logging
import os
import sys
from datetime import datetime, timedelta

import requests
import yaml

REQUEST_FMT = "https://api.github.com/repos/{0}/{1}/issues"


class Triager:
    def __init__(self, cfg):
        self.oauth_token = os.getenv("GH_TOKEN")

        # select config.yaml from cwd
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
        self.repos = []
        logging.debug("parsing orgs and repositories from config file")
        for org in config["orgs"]:
            for repo in org["repos"]:
                self.repos.append((org["name"], repo))

        # Populate maintainers list
        logging.debug("parsing list of maintainers from config file")
        self.maintainers = config["maintainers"]

        # Set address to send triage emails from
        logging.debug("parsing triager email and password from config file")
        self.sender = {
            "email": config.get("triager", {}).get("address"),
            "password": config.get("triager", {}).get("password"),
        }

        # Set last triage date
        logging.debug("setting last triage date")
        self.last_triage_date = datetime.utcnow() - timedelta(
            days=int(config["timedelta"])
        )

        logging.info("config file successfully parsed")

    def triage(self):
        issues = {}
        for org, repo in self.repos:
            repo_name = repo["name"]
            repo_labels = repo.get("labels", [])

            params = dict(since=self.last_triage_date.isoformat())
            if repo_labels:
                params["labels"] = ",".join(repo_labels)
            else:
                params["assignee"] = "none"

            issues[repo_name] = []

            logging.info(
                "requesting issue details for {0}/{1}".format(org, repo_name)
            )
            resp = requests.get(
                REQUEST_FMT.format(org, repo_name),
                params=params,
                headers=self._get_token(),
            )

            if not resp.ok:
                logging.critical(resp.json()["message"])
                return {}

            for item in resp.json():
                issues[repo_name].append(
                    {
                        "url": item["html_url"],
                        "title": item["title"],
                        "type": "Pull Request"
                        if item.get("pull_request")
                        else "Issue",
                    }
                )

        logging.info("triage successfully completed")
        return issues

    def _get_token(self):
        logging.debug("fetching oauth token")
        if self.oauth_token:
            return {"Authorization": "token {0}".format(self.oauth_token)}
