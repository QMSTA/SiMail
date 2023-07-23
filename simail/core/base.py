
from email.utils import formataddr
import smtplib


class ContentBase:
    sign = "base"
    mime_type = "*/*"


class MailBase:
    MIXED = 'mixed'
    RELATED = 'related'
    ALTRENATIVE = 'alternative'
    CHARSET = "utf-8"


class AddrBase:
    sign = "base"

    def __init__(
        self,
        email: str,
        name: None | str = None
    ) -> None:
        self._email = email
        self._name = name if name is not None else email.split("@", 1)[0]

    def __call__(self) -> str:
        return formataddr((self._name, self._email))

    @property
    def email(self):
        return self._email


class SMTPBase:
    _class = smtplib.SMTP

    def __init__(self, host: str, port: int) -> None:
        self._smtp = self._class(host=host, port=port)
        self._smtp.connect(host)
        # self._host = host
        # self._port = port

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self._smtp.quit()
            self._smtp.close()
        except smtplib.SMTPServerDisconnected:
            pass

    def send(self, mail):
        sender = mail.header.sender
        recver = mail.header.recver
        self._smtp.login(sender.email, sender.authorization)
        return self._smtp.sendmail(sender.email, [r.email for r in recver], mail.pack())
