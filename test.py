from simail import SiMail, SMTPSSLConnect
from simail.content import ImageEmbed, HTMLMessage,  FileAttachment
from simail.header import SendAddr, RecvAddr

host = "smtp.qq.com"
port = 465

sender = SendAddr("email@xxx", "xxxxxxxxxxxxx")

mail = SiMail(
    subject="我的测试邮件",
    sender=sender,
    recv_lis=[
        RecvAddr("email@xxx").type("Cc"),
    ]
)
img = ImageEmbed.new_from_file("test.jpg")
mail.append(
    img,
    FileAttachment("test.csv"),
    HTMLMessage('<img src="{}" />'.format(img))

)

with SMTPSSLConnect(host, port) as smtp:
    result = smtp.login(sender).send(mail)

print(result)
