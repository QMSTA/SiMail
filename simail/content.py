import pathlib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from .core.base import ContentBase, MailBase
import string

__all__ = [
    "HTMLMessage",
    "TEXTMessage",
    "BytesAttachment",
    "FileAttachment",
    "ImageEmbed",
    "VideoEmbed",
    "AudioEmbed"
]


class Message(ContentBase):
    CHARSET = "utf-8"

    def __init__(self, content: str) -> None:
        self.content = content

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, 'r', encoding="utf-8") as f:
            data = f.read()
        return cls(data)

    def pack(self) -> MIMEBase:
        main_type, sub_type = self.mime_type.split("/", 1)
        mime_ = MIMEBase(main_type, sub_type)
        mime_.set_payload(self.content, self.CHARSET)
        return mime_


class Embed(ContentBase):
    _RANDOM_CID_LENGTH = 6

    def __init__(self, content: bytes) -> None:
        self.content = content
        self._cid = ""

    @staticmethod
    def random_generate(length: int):
        characters = string.digits + string.ascii_uppercase
        random_id = ''.join(random.choice(characters) for _ in range(length))
        return random_id

    def update_cid(self):
        self._cid = self.random_generate(self._RANDOM_CID_LENGTH)
        return self._cid

    def pack(self) -> MIMEBase:
        main_type, sub_type = self.mime_type.split("/", 1)
        mime_ = MIMEBase(main_type, sub_type)
        mime_.set_payload(self.content)
        mime_.add_header("Content-ID", f"<{self.update_cid()}>")
        encode_base64(mime_)
        return mime_

    @property
    def cid(self):
        if self._cid == "":
            raise
        return f"cid:{self._cid}"


class Attachment(ContentBase):
    def __init__(self, content: bytes, filename: str) -> None:
        self.content = content
        self.filename = filename

    def pack(self) -> MIMEBase:
        main_type, sub_type = self.mime_type.split("/", 1)
        mime_ = MIMEBase(main_type, sub_type)
        mime_.set_payload(self.content)
        mime_.add_header('Content-Disposition', 'attachment', filename=self.filename)
        encode_base64(mime_)
        return mime_


class HTMLMessage(Message):
    sign = "cnt"
    mime_type = "text/html"


class TEXTMessage(Message):
    sign = "cnt"
    mime_type = "text/plain"


class BytesAttachment(Attachment):
    sign = "box"
    mime_type = "application/octet-stream"


class FileAttachment(Attachment):
    sign = "box"
    mime_type = "application/octet-stream"

    def __init__(self, file_path: str | pathlib.Path):
        path = pathlib.Path(file_path)
        with open(path, 'rb') as f:
            data = f.read()
        self.content = data
        self.filename = path.name


class ImageEmbed(Embed):
    sign = "msg"
    mime_type = "image/*"


class VideoEmbed(Embed):
    sign = "msg"
    mime_type = "video/*"


class AudioEmbed(Embed):
    sign = "msg"
    mime_type = "audio/*"


class MailContent(MailBase):
    """邮件内容
    """
    LIGIT_CLASS = (Message, Embed, Attachment)

    def __init__(self, header) -> None:
        # self.__box = MIMEMultipart(self.MIXED)
        # self.__msg = MIMEMultipart(self.RELATED, type="multipart/alternative")
        # self.__cnt = MIMEMultipart(self.ALTRENATIVE)
        # self.__msg.attach(self.__cnt)
        # self.__box.attach(self.__msg)

        self.__index = {
            "box": header.pack(),
            # "box": MIMEMultipart(self.MIXED),
            "msg": MIMEMultipart(self.RELATED, type="multipart/alternative"),
            "cnt": MIMEMultipart(self.ALTRENATIVE)
        }
        self.__index["msg"].attach(self.__index["cnt"])
        self.__index["box"].attach(self.__index["msg"])

    def append(self, body: Message | Embed | Attachment):
        assert isinstance(body, self.LIGIT_CLASS), "类型错误"
        item = body.pack()
        self.put(item, body.sign)

    def put(self, item, notch):
        self.__index[notch].attach(item)

    @property
    def message(self) -> MIMEMultipart:
        return self.__index["box"]
