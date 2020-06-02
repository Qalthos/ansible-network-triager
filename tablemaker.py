import textwrap

import prettytable


WRAPPER = textwrap.TextWrapper(width=80)


def make_table(data):
    table = prettytable.PrettyTable(["Repo", "Title", "URL", "Type"])
    for repo, entries in data.items():
        for entry in entries:
            entry_type = entry.pop("Type")
            for url, title in entry.items():
                table.add_row(
                    [
                        repo,
                        "\n".join(WRAPPER.wrap(text=title)),
                        "\n".join(WRAPPER.wrap(text=url)),
                        entry_type,
                    ]
                )
    return table
