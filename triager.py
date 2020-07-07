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
            repo_name = repo["name"]
            repo_labels = repo.get("labels", [])

            params = dict(since=self.last_triage_date.isoformat())
            if repo_labels:
                params["labels"] = ",".join(repo_labels)
            else:
                params["assignee"] = "none"

            issues[repo_name] = []
            resp = requests.get(
                REQUEST_FMT.format(org, repo_name),
                params=params,
                headers=self._get_token(),
            )
            if not resp.ok:
                print(resp.json()["message"])
                return {}

            for item in resp.json():
                issues[repo_name].append(
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
