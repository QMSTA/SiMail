<div align="center">

  <h1>SiMail</h1>

</div>



这是一个简单的Python项目, 旨在轻松构建高复用性的邮件实体, 以适应复杂情景的电子邮件派发需要。  

---


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