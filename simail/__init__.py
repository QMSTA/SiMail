"""
SiMail
~~~~~~

对Python标准库`email`, `smtplib`的进一步封装\n
旨在创建可复用对象. 例如发件人(`SendAddr`), 收件人(`RecvAddr`), 附件(`Attachment`派生类), 
内嵌资源(`Embed`派生类), 正文(`HTMLMessage`,`TEXTMessage`), 邮件头(`MailHeader`)

在相对复杂的场景下更能发挥作用\n

>>> from simail import SiMail, SMTPSSLConnect
>>> from simail.content import HTMLMessage
>>> from simail.header import SendAddr, RecvAddr

>>> code = "xxxxxxxxxxxx" # 密码/授权码 password/authorization
>>> sender = SendAddr("email@xxx", code, "QMStar")
>>> host, port = "smtp.xxxx.com", 465
>>> mail = SiMail(
>>>     subject="A test email",
>>>     sender=sender,
>>>     recv_lis=[RecvAddr("email@xxx").type("Cc")]
>>> )
>>> mail.append(HTMLMessage.from_file("test.html"))
>>> with SMTPSSLConnect(host, port) as smtp:
>>>     result = smtp.login(sender).send(mail)

"""


from .core.core import SiMail
from .core._smtp_ import SMTPConnect, SMTPSSLConnect
