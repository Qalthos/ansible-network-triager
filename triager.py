from datetime import datetime, timedelta
import os

import requests
import yaml


REQUEST_FMT = "https://api.github.com/repos/{0}/{1}/issues"


class Triager:
    def __init__(self, cfg="config.yaml"):
        self.oauth_token = os.getenv("GH_TOKEN")

        with open(cfg, "r") as config_file:
            config = yaml.safe_load(config_file)

        # Populate org and repos to triage
        self.repos = []
        for org in config["orgs"]:
            for repo in org["repos"]:
                self.repos.append((org["name"], repo))

        # Populate maintainers list
        self.maintainers = config["maintainers"]

        # Set address to send triage emails from
        self.sender = config["triage_address"]

        # Set last triage date
        self.last_triage_date = datetime.utcnow() - timedelta(
            days=int(config["timedelta"])
        )

    def triage(self):
        issues = {}
        for org, repo in self.repos:
            issues[repo] = []
            resp = requests.get(
                REQUEST_FMT.format(org, repo),
                params={"status": "open"},
                headers=self._get_token(),
            )
            if not resp.ok:
                print(resp.json()["message"])
                return {}

            for item in resp.json():
                if not item.get("assignee"):
                    created_at = datetime.strptime(
                        item["created_at"], "%Y-%m-%dT%H:%M:%SZ"
                    )
                    if created_at >= self.last_triage_date:
                        issues[repo].append(
                            {
                                "url": item["html_url"],
                                "title": item["title"],
                                "type": "Pull Request" if item.get("pull_request") else "Issue",
                            }
                        )

        return issues

    def _get_token(self):
        if self.oauth_token:
            return {"Authorization": "token {0}".format(self.oauth_token)}
