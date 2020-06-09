from datetime import date
from email.message import EmailMessage
from email.headerregistry import Address
import smtplib


def send_mail(content, sender, receivers=[]):
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = _get_recipients(receivers)
    msg["Subject"] = f"Ansible Network Weekly Triage - {date.today().isoformat()}"
    msg.set_content(str(content))
    msg.add_alternative(
        content.get_html_string(
            attributes={"border": 1, "style": "text-align:center"}
        ),
        subtype="html"
    )

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(sender, "")
        smtp.send_message(msg)


def _get_recipients(receivers):
    return [
        Address(item["name"], addr_spec=item["email"])
        for item in receivers
    ]
