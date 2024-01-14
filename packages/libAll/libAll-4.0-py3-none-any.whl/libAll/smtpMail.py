import smtplib
from email.mime.text import MIMEText


class smtpMail_C():
    soutput = True
    output = False
    host = None
    mail = None

    """setting mail or google"""
    def __init__(self, setting=None, address="smtp.gmail.com", port=587, sec_type="tls"):
        try:
            if setting == "mail":
                self.host = smtplib.SMTP_SSL("smtp.mail.ru", 465)

            else:
                if sec_type == "tls":
                    self.host = smtplib.SMTP(address, port)
                    self.host.starttls()
                elif sec_type == "ssl":
                    self.host = smtplib.SMTP_SSL(address, port)


        except Exception as ex:
            self.output = ('error ', ex)

    def login(self, email, password):
        try:
            self.mail = email
            self.host.login(email, password)
        except Exception as ex:
            if self.soutput == True:
                return ('error ', ex)
            else:
                self.output = ('error ', ex)
                return "error"

    def send(self, from_mail, to_mail, subject_text, message_text):
        try:
            msg = MIMEText(message_text)
            msg["Subject"] = subject_text
            self.host.sendmail(from_mail, to_mail, msg.as_string())
        except Exception as ex:
            if self.soutput == True:
                return ('error ', ex)
            else:
                self.output = ('error ', ex)
                return "error"
