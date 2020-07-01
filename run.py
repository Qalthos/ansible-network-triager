from triager import Triager
from tablemaker import make_table
from mailer import send_mail


if __name__ == "__main__":
    triager = Triager()
    print("Gathering issues for triage...")
    issues = triager.triage()

    if issues:
        table = make_table(issues)
        print(table)

        print("Mailing table to maintainers...")
        send_mail(
            content=table,
            sender=triager.sender,
            receivers=triager.maintainers,
        )
