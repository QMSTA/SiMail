import smtplib
from .base import SMTPBase


class SMTPConnect(SMTPBase):
    """
    SMTPConnect

    使用`smtplib.SMTP`, 构建基本的smtp连接
    """
    _class = smtplib.SMTP


class SMTPSSLConnect(SMTPBase):
    """
    SMTPSSLConnect

    使用`smtplib.SMTP_SSL`, 构建基本的smtp连接
    """
    _class = smtplib.SMTP_SSL
