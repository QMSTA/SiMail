from collections import defaultdict
from email.mime.multipart import MIMEMultipart
from .base import MailBase, AddrBase
from typing import List, Literal

__all__ = [
    "SendAddr",
    "RecvAddr",
    "MailHeader"
]


class SendAddr(AddrBase):
    """
    `SendAddr`: 发件人

    >>> code = "xxxxxxxxxx" # 授权码
    >>> sender = SendAddr("email@xxx", code, "Email")
    """
    _sign = "send"

    def __init__(self, email: str, authorization_code: str, name: str | None = None) -> None:
        """
        email: str 邮箱
        authorization_code: str 密码/授权码
        name: str|None 发件人姓名, 可不填, 默认为邮箱@符号前一部分的字符串
        """
        self._email = email
        self._name = name if name is not None else email.split("@", 1)[0]
        self._a_code = authorization_code

    @property
    def authorization(self) -> str:
        """授权码"""
        return self._a_code


class RecvAddr(AddrBase):
    """
    `RecvAddr`: 收件人

    >>> recvs = [
    >>>     RecvAddr("email@xxx", "Email"),
    >>>     ...
    >>> ]
    """
    _sign = "recv"
    types = ("Cc", "To", "Bcc")
    TO = "To"
    CC = "Cc"
    BCC = "Bcc"

    def __init__(self, email: str, name: str | None = None) -> None:
        """
        email: str 邮箱
        name: str|None 收件人姓名, 可不填, 默认为邮箱@符号前一部分的字符串
        """
        super().__init__(email, name)
        self._type = self.TO

    def type(self, type_: Literal["Cc", "To", "Bcc"]) -> "RecvAddr":
        """
        "To" (defulte)
        "Cc" 抄送
        "Bcc" 密送

        通过传入参数设置该收件人类型, 该函数返回收件人对象实例
        """
        if type_ not in self.types:
            raise
        self._type = type_
        return self


class MailHeader(MailBase):
    """
    `MailHeader`: 邮件头

    >>> head = MailHeader(...)
    >>> mail = SiMail.new_from_header(head)
    >>> ...

    一般情况下, 没有邮件头复用的需要的话, 不需要显示的实例化该类
    """

    def __init__(self, subject: str, sender: SendAddr, recv_lis: List[RecvAddr]) -> None:
        """
        subject: str 邮箱
        sender: SendAddr 发件人
        recv_lis: List[RecvAddr] 收件人列表
        """
        self._subject = subject
        self._send = sender
        self._recvs = recv_lis
        self._head = MIMEMultipart(self.MIXED)

    def pack(self):
        """
        MailHeader.pack()

        返回打包好的邮件头信息
        """
        dic = defaultdict(list)
        self._head["Subject"] = self._subject
        self._head["From"] = self._send()
        # 将不同种类的收件人分类
        for recv in self._recvs:
            dic[recv._type].append(recv())

        # 按分类将收件人加入到对应的头信息里
        for k, val_lis in dic.items():
            self._head[k] = ",".join(val_lis)

        return self._head

    @property
    def recver(self) -> List[RecvAddr]:
        """收件人对象实例列表"""
        return self._recvs

    @property
    def sender(self) -> SendAddr:
        """发件人对象实例"""
        return self._send

    @property
    def recv_emails(self) -> List[str]:
        """收件人邮箱列表"""
        return [r.email for r in self.recver]

    @property
    def sender_email(self) -> str:
        """发件人邮箱"""
        return self.sender.email
