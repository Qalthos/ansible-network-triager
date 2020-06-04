from triager import Triager
from tablemaker import TableMaker
from mailer import send_mail


if __name__ == "__main__":
    triager = Triager()
    triager.triage()
    table = TableMaker(triager.triaged_data).make_table()
    send_mail(
        content=table,
        receivers=triager.maintainers,
    )
