import os
import json
from datetime import datetime, timedelta

import requests
import yaml

REQUEST_FMT = "https://api.github.com/repos/{0}/{1}/issues"


class Triager:
    def __init__(self, cfg="config.yaml"):
        self.cfg = cfg
        self.org = None
        self.repos = []
        self.maintainers = []
        self.last_triage_date = None
        self.oauth_token = os.getenv("GH_TOKEN")
        self.triaged_data = {}
        self.load_config()

    def load_config(self):
        with open(self.cfg, "r") as config_file:
            try:
                cfg = yaml.safe_load(config_file)
            except yaml.YAMLError as e:
                raise e

        # Populate org and repos to triage
        self.org = cfg["org"]
        for repo in cfg["repos"]:
            self.repos.append(repo)

        # Populate maintainers list
        for maintainer in cfg["maintainers"]:
            self.maintainers.append(
                {"name": maintainer["name"], "email": maintainer["email"]}
            )

        # Set last triage date
        self.last_triage_date = datetime.utcnow() - timedelta(
            days=int(cfg["timedelta"])
        )

        # pre-populate the final triaged data dict
        for item in self.repos:
            self.triaged_data.update({item: []})

    def triage(self):
        for repo in self.repos:
            resp = requests.get(
                REQUEST_FMT.format(self.org, repo),
                params={"status": "open"},
                headers=self._get_token(),
            )
            for item in resp.json():
                if not item.get("assignee"):
                    # The ISO-8601 standard (format in which the API returns the dates)
                    # allows “Z” to be used instead of the zero offset, but
                    # fromisoformat() cannot parse this.
                    created_at = datetime.fromisoformat(
                        item["created_at"].replace("Z", "")
                    )
                    if created_at >= self.last_triage_date:
                        # Issue/PR URL will always be unique and we can key on that
                        self.triaged_data[repo].append(
                            {item["html_url"]: item["title"]}
                        )

    def _get_token(self):
        if self.oauth_token:
            return {"Authorization": "token {0}".format(self.oauth_token)}
