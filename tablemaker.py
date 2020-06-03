import prettytable
import textwrap


class TableMaker:
    def __init__(self, data):
        self.data = data
        self.wrapper = textwrap.TextWrapper(width=80)
        self.table = prettytable.PrettyTable(["Repo", "Title", "URL", "Type"])

    def make_table(self):
        for repo, values in self.data.items():
            for entry in values:
                entry_type = entry.pop("Type")
                for url, title in entry.items():
                    self.table.add_row(
                        [
                            repo,
                            "\n".join(self.wrapper.wrap(text=title)),
                            "\n".join(self.wrapper.wrap(text=url)),
                            entry_type,
                        ]
                    )
        return self.table
