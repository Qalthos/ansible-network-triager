import textwrap
from typing import Dict, List

import prettytable

from triager.triager import Issue


WRAPPER = textwrap.TextWrapper(width=80)


def make_table(data: Dict[str, List[Issue]]) -> prettytable.PrettyTable:
    table = prettytable.PrettyTable(["Repo", "Title", "URL", "Type"])
    for repo, entries in data.items():
        for entry in entries:
            table.add_row(
                [
                    repo,
                    "\n".join(WRAPPER.wrap(text=entry["title"])),
                    "\n".join(WRAPPER.wrap(text=entry["url"])),
                    entry["type"],
                ]
            )
    return table
