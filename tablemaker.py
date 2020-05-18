import prettytable
from textwrap import wrap


class TableMaker:
    def __init__(self, data):
        self.data = data
        self.table = prettytable.PrettyTable(["Repo", "Title", "Issue Link"])

    def make_table(self):
        for repo, values in self.data.items():
            for entry in values:
                for url, title in entry.items():
                    self.table.add_row(
                        [
                            repo,
                            "\n".join(wrap(text=title)),
                            "\n".join(wrap(text=url)),
                        ]
                    )
        return self.table
