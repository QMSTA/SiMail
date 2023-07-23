import smtplib
from .base import SMTPBase


class SMTPConnect(SMTPBase):
    _class = smtplib.SMTP


class SMTPSSLConnect(SMTPBase):
    _class = smtplib.SMTP_SSL
