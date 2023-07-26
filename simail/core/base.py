
from email.utils import formataddr
from .. import exception
import smtplib


class ContentBase:
    _sign = "base"
    mime_type = "*/*"


class MailBase:
    MIXED = 'mixed'
    RELATED = 'related'
    ALTRENATIVE = 'alternative'
    CHARSET = "utf-8"


class AddrBase:
    _sign = "base"

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
        if exc_type is smtplib.SMTPServerDisconnected:
            raise exception.SMTPContentError(f"{exc_value}; 检查邮箱发送账号和密码/授权码") from None

        try:
            self._smtp.quit()
            self._smtp.close()
        except smtplib.SMTPServerDisconnected as exc:
            raise exception.SMTPContentError(f"{exc}; smtp服务未连接") from None

    def login(self, sender):
        self._smtp.login(sender.email, sender.authorization)
        return self

    def send(self, mail):
        sender = mail.header.sender_email
        recver = mail.header.recv_emails
        mail_pack = mail.pack()
        return self._smtp.sendmail(sender, recver, mail_pack)
