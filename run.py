from triager import Triager
from tablemaker import make_table
from mailer import send_mail


if __name__ == "__main__":
    triager = Triager()
    triager.triage()
    table = make_table(triager.triaged_data)
    send_mail(
        content=table,
        sender=triager.sender,
        receivers=triager.maintainers,
    )
