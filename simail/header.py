"""
Simail.header
~~~~~~~~~~~~~

`SendAddr`: 发件人地址 \n
`RecvAddr`: 收件人地址 \n
`MailHeader`: 邮件头, 如果有邮件头复用的需要, 可以使用如下方法构建邮件体: \n
>>> head = MailHeader(...)
>>> mail = SiMail.new_from_header(head)
>>> ...
"""

from .core._header import SendAddr, RecvAddr, MailHeader
