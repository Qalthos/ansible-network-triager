import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mailer:
    def __init__(self, content=None, receivers=[]):
        self.smpt_session = smtplib.SMTP("smtp.gmail.com", 587)
        self.content = content
        self.subject = "Ansible Network Weekly Triage - {0}".format(
            datetime.utcnow().strftime("%Y/%m/%d")
        )
        self.recepients = self._get_recepients(receivers)

    def send_mail(self):
        self.smpt_session.starttls()
        self.smpt_session.login("", "")

        msg = MIMEMultipart("alternative")
        msg["To"] = ", ".join(self.recepients)
        msg["Subject"] = self.subject
        msg.attach(MIMEText(self.content, "html"))

        self.smpt_session.sendmail("", self.recepients, msg.as_string())
        self.smpt_session.quit()

    def _get_recepients(self, receivers):
        recepients = []
        for item in receivers:
            recepients.append(item["email"])
        return recepients
