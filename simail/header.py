from collections import defaultdict
from email.mime.multipart import MIMEMultipart

from .core.base import MailBase, AddrBase
from typing import List, Literal


class SendAddr(AddrBase):
    sign = "send"

    def __init__(self, email: str, authorization_code: str, name: str | None = None) -> None:
        self._email = email
        self._name = name if name is not None else email.split("@", 1)[0]
        self._a_code = authorization_code

    @property
    def authorization(self):
        return self._a_code

    


class RecvAddr(AddrBase):
    sign = "recv"
    types = ("Cc", "To", "Bcc")
    TO = "To"
    CC = "Cc"
    BCC = "Bcc"

    def __init__(self, email: str, name: str | None = None) -> None:
        super().__init__(email, name)
        self._type = self.TO

    def type(self, type_: Literal["Cc", "To", "Bcc"]) -> "RecvAddr":
        """
        "To" (defulte)
        "Cc" 抄送
        "Bcc" 密送
        """
        if type_ not in self.types:
            raise
        self._type = type_
        return self


class MailHeader(MailBase):
    def __init__(self, subject: str, sender: SendAddr, recv_lis: List[RecvAddr]) -> None:
        self._subject = subject
        self._send = sender
        self._recvs = recv_lis
        self._head = MIMEMultipart(self.MIXED)

    def pack(self):
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
    def recvs(self) -> List[str]:
        return [r() for r in self._recvs]

    @property
    def recver(self) -> List[RecvAddr]:
        return self._recvs

    @property
    def sender(self) -> SendAddr:
        return self._send
