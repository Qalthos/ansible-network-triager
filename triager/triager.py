import logging
import os

import requests

from triager.config import load_config

REQUEST_FMT = "https://api.github.com/repos/{0}/{1}/issues"


class Triager:
    def __init__(self, cfg):
        self.oauth_token = os.getenv("GH_TOKEN")
        parsed_config = load_config(cfg)
        self.repos = parsed_config["repos"]
        self.maintainers = parsed_config["maintainers"]
        self.last_triage_date = parsed_config["last_triage_date"]
        self.sender = parsed_config["sender"]

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
