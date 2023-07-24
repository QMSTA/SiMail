from ..content import MailContent, Attachment, Embed, Message
from ..header import MailHeader, SendAddr, RecvAddr
from typing import List

__all__ = [
    "SiMail"
]


class SiMail:
    def __init__(
        self,
        subject: str,
        sender: SendAddr,
        recv_lis: List[RecvAddr]
    ) -> None:

        self._header = MailHeader(subject=subject, sender=sender, recv_lis=recv_lis)
        self._content = MailContent(self._header)

    def append(self, *body: Attachment | Embed | Message):
        for b in body:
            self._content.append(b)

    def pack(self) -> str:
        return self._content.message.as_string()

    @classmethod
    def new_from_header(cls, header: MailHeader) -> "SiMail":
        return cls(header._subject, header._send, header._recvs)

    @property
    def header(self):
        return self._header

    @property
    def content(self):
        return self._content
