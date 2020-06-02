from triager.triager import Triager
from triager.tablemaker import make_table
from triager.mailer import send_mail

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
