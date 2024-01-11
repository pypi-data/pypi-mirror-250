# 发网消息通知组件

## 发送企业微信消息
```python
from FineEx.Middleware.Message.pywechat import WorkChatSender
def weChat():
    corpid = 'corpid'
    corpsecret = 'corpsecret'
    agentid = '1000039'
    workSender = WorkChatSender(corpid=corpid, corpsecret=corpsecret, agentid=agentid)
    workSender.send_text("hello", touser='91237')
    subject = '测试异常'
    message = f"""
        >**测试信息异常** 
        请尽快处理！
        查看详情，请点击：[FineEx](https://www.fineex.net)
        """
    workSender.send_markdown(subject + "\n" + message.strip())
    workSender.send_image(r"iamge_path", touser='receiver')
    workSender.send_file(r"file_path", touser='receiver')
    workSender.send_video(r"video_path", touser='receiver')
    workSender.send_voice(r"voice_path", touser='receiver')
```
[企业微信消息通知官方文档](https://developer.work.weixin.qq.com/document/path/90248)
## 发送网易邮件
```python
from FineEx.Middleware.Message.pyemail import MailSender
def Mail():
    # 普通文本邮件
    sml1 = MailSender('sender', 'yourpassword', 'smtp.qiye.163.com:465')
    sml1.setMailInfo('receiver', '测试标题', '测试正文', 'plain')
    sml1.sendMail()

    # html文件带文件
    sml2 = MailSender('sender', 'yourpassword', 'smtp.qiye.163.com:465')
    content = sml2.generateHtml('告警', '测试告警标题', '张三', '测试告警内容')
    sml2.setMailInfo('receiver', '测试标题', content, 'html', r'file_path')
    sml2.sendMail()
```
## 发送pushdeer消息
```python
from FineEx.Middleware.Message.pypushdeer import PushDeerSender
def pushDeer():
    pushdeer = PushDeerSender(pushkey="pushkey")
    pushdeer.send_text("hello world", desp="optional description")
    pushdeer.send_markdown("# hello world", desp="**optional** description in markdown")
    pushdeer.send_image("https://github.com/easychen/pushdeer/raw/main/doc/image/clipcode.png")
    pushdeer.send_image(
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVQYV2NgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII=")
```
[pushdeer项目地址](https://github.com/easychen/pushdeer)
## 通过阿里云短信服务发送消息
```python
from FineEx.Middleware.Message.pysms import SmsSender
def Sms():
    ACCESS_KEY_ID = ''
    ACCESS_KEY_SECRET = ''
    SIGN_NAME = ''
    template_code = ''
    PhoneNumber = ''
    msg = {
        "mgs": "服务器192.168.1.1异常，系统CPU过高，当前值100%",
        "outer": "test"
    }
    sms = SmsSender(ACCESS_KEY_ID, ACCESS_KEY_SECRET, SIGN_NAME, template_code)
    sms.sendSms(PhoneNumber, **msg)
```
[阿里云短息服务地址](https://next.api.aliyun.com/api/Dysmsapi/2017-05-25/SendSms?spm=5176.25163407.overview-index-9c3d4_4cfbe_0.25.545abb6e1aS01u&sdkStyle=dara&tab=DOC&lang=PYTHON)
## 电话通知
```python
from FineEx.Middleware.Message.pyphone import PhoneCaller
def Call():
    caller = PhoneCaller('account', 'password')
    msg = '机房温度异常：嘉合机房当前温度30度，请尽快安排人员排查情况'
    mobile = '17601234567'
    print(caller.call(msg, mobile))
```
[互亿无线](https://www.ihuyi.com/api/voice_notice.html)