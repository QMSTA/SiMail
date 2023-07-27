<div align="center">
  <h1>SiMail</h1>
</div>


这是一个简单的Python项目, 旨在轻松构建高复用性的邮件实体, 以适应复杂情景的电子邮件派发需要。  

---


## 特点

1. **高度可定制**：通过提供多个类别的对象，你可以根据实际需求构建符合你要求的邮件内容，使邮件发送变得灵活和易于定制。
 
2. **多情景支持**：不同的应用场景可能需要不同类型的邮件，该项目提供了发件人、收件人、附件、内嵌资源、HTML正文和纯文本正文等组件，以满足各种情景的需要。
 
3. **简单易用**：项目提供了清晰的接口和示例代码，使你能够快速上手，并且在你的应用程序中轻松地发送电子邮件。
  

## 安装

```
git clone https://github.com/QMSTA/SiMail.git
```


## 开始使用

``` python
from simail import SiMail, SMTPSSLConnect
from simail.content import ImageEmbed, HTMLMessage, FileAttachment
from simail.header import SendAddr, RecvAddr

code = "xxxxxxxxxxxx" # 密码/授权码 password/authorization
sender = SendAddr("email@xxx", code, "QMStar")
host, port = "smtp.xxxx.com", 465
mail = SiMail(
	subject="A test email",
	sender=sender,
    recv_lis=[RecvAddr("email@xxx").type("Cc")]
)
img = ImageEmbed(...)
mail.append(
	img,
	FileAttachment(...),
	HTMLMessage("<img src={} />".format(img.cid)),
	...
)
with SMTPSSLConnect(host, port) as smtp:
    result = smtp.login(sender).send(mail)
```
在实际使用中，你需要根据实际情况填写发件人邮箱和密码/授权码，并可能需要配置SMTP服务器信息。

## 贡献

欢迎贡献代码！如果你发现bug，有改进意见，或者希望添加新的邮件组件，请提交Pull Request。