from triager import Triager
from tablemaker import TableMaker
from prettytable import ALL
from mailer import Mailer

if __name__ == "__main__":
    triager = Triager()
    triager.triage()
    table = TableMaker(triager.triaged_data).make_table()
    Mailer(
        content=table.get_html_string(), receivers=triager.maintainers
    ).send_mail()
