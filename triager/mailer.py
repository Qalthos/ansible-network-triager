import logging
import smtplib
from datetime import date
from email.message import EmailMessage


def send_mail(content, config):
    logging.info("attempting to send email to maintainers")

    msg = EmailMessage()
    msg["From"] = config.sender["email"]
    msg["To"] = config.maintainers
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
        smtp.login(config.sender["email"], config.sender["password"])
        smtp.send_message(msg)

    logging.info("email sent successfully")
