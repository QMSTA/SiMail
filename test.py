from simail import SiMail, SMTPSSLConnect
from simail.content import HTMLMessage, FileAttachment
from simail.header import SendAddr, RecvAddr
code = "XXXXXXXXXXXXXXXXX"  # 授权码
host = "smtp.qq.com"
port = 465

with SMTPSSLConnect(host, port) as smtp:
    mail = SiMail(
        subject="This is a test email!",
        sender=SendAddr("qmstar0@qq.com", code, "QMStar"),
        recv_lis=[RecvAddr("qmstar0@qq.com")]
    )
    mail.append(
        HTMLMessage.from_file("test.html"),
        FileAttachment("test.jpg")
    )
    result = smtp.send(mail)
