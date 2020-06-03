from triager import Triager
from tablemaker import TableMaker
from mailer import Mailer
from prettytable import PLAIN_COLUMNS

if __name__ == "__main__":
    triager = Triager()
    triager.triage()
    table = TableMaker(triager.triaged_data).make_table()
    Mailer(
        content=table.get_html_string(
            attributes={"border": 1, "style": "text-align:center"}
        ),
        receivers=triager.maintainers,
    ).send_mail()
