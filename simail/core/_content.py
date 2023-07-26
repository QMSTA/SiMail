import pathlib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from .base import ContentBase, MailBase
import string
from .. import util

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
    def new_from_file(cls, file_path: str | pathlib.Path):
        """从文件读取内容构建邮件正文"""
        with open(file_path, 'r', encoding="utf-8") as f:
            data = f.read()
        return cls(data)

    def pack(self) -> MIMEBase:
        """由相关内容构建一个`MIMEBase`实例并返回"""
        main_type, sub_type = self.mime_type.split("/", 1)
        mime_ = MIMEBase(main_type, sub_type)
        mime_.set_payload(self.content, self.CHARSET)
        return mime_


class Embed(ContentBase):
    _RANDOM_CID_LENGTH = 6  # 随机cid字符串的长度

    def __init__(self, content: bytes, cid: str = "") -> None:
        self.content = content
        self._cid = cid if cid else self.update_cid()

    @classmethod
    def new_from_file(cls, file_path: str | pathlib.Path, cid: str = ""):
        """从文件读取数据构建内嵌资源对象"""
        with open(file_path, 'rb') as f:
            data = f.read()
        return cls(data, cid)

    @staticmethod
    def random_generate(length: int):
        """生成随机字符"""
        characters = string.digits + string.ascii_uppercase
        random_id = ''.join(random.choice(characters) for _ in range(length))
        return random_id

    def update_cid(self):
        """为该实例设置一个唯一cid作为内嵌资源在html中的索引"""
        self._cid = self.random_generate(self._RANDOM_CID_LENGTH)
        return self._cid

    def pack(self) -> MIMEBase:
        """由相关内容构建一个`MIMEBase`实例并返回"""
        main_type, sub_type = self.mime_type.split("/", 1)
        mime_ = MIMEBase(main_type, sub_type)
        mime_.set_payload(self.content)
        encode_base64(mime_)
        mime_.add_header("Content-ID", f"<{self._cid}>")
        return mime_

    def __repr__(self) -> str:
        return self.cid

    @property
    def cid(self):
        """返回cid"""
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
        encode_base64(mime_)
        mime_.add_header('Content-Disposition', 'attachment', filename=util.base64_encode_filename(self.filename))
        return mime_


class HTMLMessage(Message):
    """
    HTMLMessage

    构建html正文
    >>> html_body = TEXTMessage(...)
    >>> mail = SiMail(...)
    >>> mail.append(html_body)
    >>> ...
    """
    _sign = "cnt"
    mime_type = "text/html"


class TEXTMessage(Message):
    """
    TEXTMessage

    构建text正文
    >>> text_body = TEXTMessage(...)
    >>> mail = SiMail(...)
    >>> mail.append(text_body)
    >>> ...
    """
    _sign = "cnt"
    mime_type = "text/plain"


class BytesAttachment(Attachment):
    """
    BytesAttachment

    将byte数据直接作为邮件附件, 但仍需要指定文件名以在收件人客户端显示
    >>> data = b"..."  # 从网络上爬虫或从其他程序获取的文件数据
    >>> attachment = BytesAttachment(data, filename="xxxx.png")
    >>> mail = SiMail(...)
    >>> mail.append(data)
    >>> ...
    """
    _sign = "box"
    mime_type = "application/octet-stream"

    def __init__(self, content: bytes, filename: str) -> None:
        super().__init__(content, filename)


class FileAttachment(Attachment):
    """
    FileAttachment

    将文件作为邮件附件发送
    >>> attachment = FileAttachment("/your/path/xxxx.png")
    >>> mail = SiMail(...)
    >>> mail.append(data)
    >>> ...
    """
    _sign = "box"
    mime_type = "application/octet-stream"

    def __init__(self, file_path: str | pathlib.Path):
        path = pathlib.Path(file_path)
        with open(path, 'rb') as f:
            data = f.read()
        self.content = data
        self.filename = path.name
        print(self.filename)


class ImageEmbed(Embed):
    """
    ImageEmbed

    内嵌图片资源
    >>> data = b"..."  # 文件数据或其他
    >>> html_str = '<img src="{}" />'
    >>> embed = ImageEmbed(data)
    >>> mail = SiMail(...)
    >>> mail.append(
    >>>     embed,
    >>>     HTMLMessage(html_str.format(mail.cid))
    >>> )
    >>> ...
    """
    _sign = "msg"
    mime_type = "image/*"


# TODO: video标签无法实现内嵌
class VideoEmbed(Embed):
    _sign = "msg"
    mime_type = "video/*"

# TODO: audio标签无法实现内嵌


class AudioEmbed(Embed):
    _sign = "msg"
    mime_type = "audio/mpeg"


class MailContent(MailBase):
    """
    邮件体
    """
    LIGIT_CLASS = (Message, Embed, Attachment)

    def __init__(self, header) -> None:
        self.__index = {
            "box": header.pack(),
            "msg": MIMEMultipart(self.RELATED, type="multipart/alternative"),
            "cnt": MIMEMultipart(self.ALTRENATIVE)
        }
        self.__index["msg"].attach(self.__index["cnt"])
        self.__index["box"].attach(self.__index["msg"])

    def append(self, body: Message | Embed | Attachment):
        assert isinstance(body, self.LIGIT_CLASS), "类型错误"
        item = body.pack()
        self.put(item, body._sign)

    def put(self, item, notch):
        self.__index[notch].attach(item)

    @property
    def message(self) -> MIMEMultipart:
        return self.__index["box"]
