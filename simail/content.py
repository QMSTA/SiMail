"""
SiMail.content
~~~~~~~~~~~~~~

邮件内容分为: 附件(`Attachment`), 正文(`Message`), 内嵌资源(`Embed`)

>>> mail = SiMail(...)
>>> mail.append(
>>>     HTMLMessage(...),
>>>     FileAttachment(...),
>>>     ...
>>> )
>>> ...

内嵌资源(`Embed`)主要使用在HTML正文中, 以页面资源的形式直接显示; 内嵌资源需要与HTMLMessage搭配使用

所有邮件内容均不可使用基类, 而是使用其派生类
"""


from .core._content import (
    FileAttachment, BytesAttachment,
    ImageEmbed,
    # VideoEmbed, AudioEmbed,  # 经测试, audio和video标签暂时无法实现内嵌资源
    HTMLMessage, TEXTMessage
)
