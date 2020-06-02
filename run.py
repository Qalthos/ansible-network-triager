from triager import Triager
from tablemaker import make_table
from mailer import send_mail


if __name__ == "__main__":
    triager = Triager()
    issues = triager.triage()

    if issues:
        table = make_table(issues)
        send_mail(
            content=table,
            sender=triager.sender,
            receivers=triager.maintainers,
        )
