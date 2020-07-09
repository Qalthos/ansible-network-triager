import logging
import smtplib
from datetime import date
from email.headerregistry import Address
from email.message import EmailMessage


def send_mail(content, sender, receivers=[]):
    logging.info("attempting to send email to maintainers")

    if not sender.get("email") or not sender.get("password"):
        logging.critical(
            "Triager email or password missing from config file, email could not be sent"
        )
    else:
        msg = EmailMessage()
        msg["From"] = sender["email"]
        msg["To"] = _get_recipients(receivers)
        msg["Subject"] = "Ansible Network Weekly Triage - {0}".format(
            date.today().isoformat()
        )
        msg.set_content(str(content))
        msg.add_alternative(
            content.get_html_string(
                attributes={"border": 1, "style": "text-align:center"}
            ),
            subtype="html",
        )

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            logging.info("attempting to send email")
            smtp.starttls()
            smtp.login(sender["email"], sender["password"])
            smtp.send_message(msg)

        logging.info("email sent successfully")


def _get_recipients(receivers):
    logging.info("generating list of receipients")
    return [
        Address(item["name"], addr_spec=item["email"]) for item in receivers
    ]
