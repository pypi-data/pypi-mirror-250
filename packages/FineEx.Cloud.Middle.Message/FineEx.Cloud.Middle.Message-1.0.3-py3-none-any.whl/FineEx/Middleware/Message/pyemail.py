# -*- coding: utf-8 -*-
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from email.header import Header


class MailSender:
    def __init__(self, user, passwd, smtp):
        """
        构造函数
        :param user: 用户名
        :param passwd: 密码
        :param smtp: smtp服务器地址，带端口
        :param port: 端口
        :param usettls:
        """
        self.mailUser = user
        self.mailPassword = passwd
        self.smtpServer = smtp
        self.mailServer = smtplib.SMTP_SSL(self.smtpServer)
        self.mailServer.login(self.mailUser, self.mailPassword)
        self.msg = MIMEMultipart()

    def __del__(self):
        """
        对象销毁时，关闭mailserver
        :return:
        """
        self.mailServer.quit()

    def setMailInfo(self, receiveUser, subject, text, text_type, *attachmentFilePaths):
        """
        设置邮件的基本信息
        :param receiveUser: 收件人邮箱
        :param subject: 主题
        :param text: 正文
        :param text_type: 正文类型，html或者plain
        :param attachmentFilePaths: 可变参数，附件路径列表
        :return:
        """
        self.msg['From'] = self.mailUser
        self.msg['To'] = receiveUser

        self.msg['Subject'] = subject
        self.msg.attach(MIMEText(text, text_type))
        for attachmentFilePath in attachmentFilePaths:
            self.msg.attach(self.getAttachmentFromFile(attachmentFilePath))

    def generateHtml(self, messgType, title, receiverName, content):
        template = f"""
        <div>
  <includetail>
    <div align="center">
      <div
        class="open_email"
        style="
          margin-left: 8px;
          margin-top: 8px;
          margin-bottom: 8px;
          margin-right: 8px;
        "
      >
        <div>
          <br />
          <span class="genEmailContent">
            <div
              id="cTMail-Wrap"
              style="
                word-break: break-all;
                box-sizing: border-box;
                text-align: center;
                min-width: 320px;
                max-width: 660px;
                border: 1px solid #f6f6f6;
                background-color: #f7f8fa;
                margin: auto;
                padding: 20px 0 30px;
                font-family: 'helvetica neue', PingFangSC-Light, arial,
                  'hiragino sans gb', 'microsoft yahei ui', 'microsoft yahei',
                  simsun, sans-serif;
              "
            >
              <div class="main-content" style="">
                <table
                  style="
                    width: 100%;
                    font-weight: 300;
                    margin-bottom: 10px;
                    border-collapse: collapse;
                  "
                >
                  <tbody>
                    <tr style="font-weight: 300">
                      <td style="width: 3%; max-width: 30px"></td>
                      <td style="max-width: 600px">
                        <div id="cTMail-logo" style="width: 92px; height: 25px">
                          <a href="https://www.fineex.com">
                            <img
                              border="0"
                              src="https://www.fineex.com/Public/Uploads/uploadfile/images/20190610/20190610100102_5cfdb9de68df2.png"
                              style="width: 152px; height: 20px; display: block"
                            />
                          </a>
                        </div>
                        <p
                          style="
                            height: 2px;
                            background-color: #fc5319;
                            border: 0;
                            font-size: 0;
                            padding: 0;
                            width: 100%;
                            margin-top: 20px;
                          "
                        ></p>

                        <div
                          id="cTMail-inner"
                          style="
                            background-color: #fff;
                            padding: 23px 0 20px;
                            box-shadow: 0px 1px 1px 0px rgba(122, 55, 55, 0.2);
                            text-align: left;
                          "
                        >
                          <table
                            style="
                              width: 100%;
                              font-weight: 300;
                              margin-bottom: 10px;
                              border-collapse: collapse;
                              text-align: left;
                            "
                          >
                            <tbody>
                              <tr style="font-weight: 300">
                                <td style="width: 3.2%; max-width: 30px"></td>
                                <td style="max-width: 480px; text-align: left">
                                  <h1
                                    id="cTMail-title"
                                    style="
                                      font-size: 20px;
                                      line-height: 36px;
                                      margin: 0px 0px 22px;
                                    "
                                  >
                                    【{messgType}】{title}
                                  </h1>

                                  <p
                                    id="cTMail-userName"
                                    style="
                                      font-size: 14px;
                                      color: #333;
                                      line-height: 24px;
                                      margin: 0;
                                    "
                                  >
                                    尊敬的{receiverName}，您好！
                                  </p>

                                  <p
                                    class="cTMail-content"
                                    style="
                                      line-height: 24px;
                                      margin: 6px 0px 0px;
                                      overflow-wrap: break-word;
                                      word-break: break-all;
                                    "
                                  >
                                    <span
                                      style="
                                        color: rgb(51, 51, 51);
                                        font-size: 14px;
                                      "
                                    >
                                        {content}
                                    </span>
                                  </p>

                                  <dl
                                    style="
                                      font-size: 14px;
                                      color: rgb(51, 51, 51);
                                      line-height: 18px;
                                    "
                                  >
                                    <dd
                                      style="
                                        margin: 0px 0px 6px;
                                        padding: 0px;
                                        font-size: 12px;
                                        line-height: 22px;
                                      "
                                    >
                                      <p
                                        id="cTMail-sender"
                                        style="
                                          font-size: 14px;
                                          line-height: 26px;
                                          word-wrap: break-word;
                                          word-break: break-all;
                                          margin-top: 32px;
                                        "
                                      >
                                        此致
                                        <br />
                                        <strong>发网科技数仓团队</strong>
                                      </p>
                                    </dd>
                                  </dl>
                                </td>
                                <td style="width: 3.2%; max-width: 30px"></td>
                              </tr>
                            </tbody>
                          </table>
                        </div>
                        <div
                          id="cTMail-copy"
                          style="
                            text-align: center;
                            font-size: 12px;
                            line-height: 18px;
                            color: #999;
                          "
                        >
                          <table
                            style="
                              width: 100%;
                              font-weight: 300;
                              margin-bottom: 10px;
                              border-collapse: collapse;
                            "
                          >
                            <tbody>
                              <tr style="font-weight: 300">
                                <td style="width: 3.2%; max-width: 30px"></td>
                                <td style="max-width: 540px">
                                  <p
                                    style="
                                      text-align: center;
                                      margin: 20px auto 14px auto;
                                      font-size: 12px;
                                      color: #999;
                                    "
                                  >
                                    此为系统邮件，请勿回复。
                                  </p>
                                  <p
                                    id="cTMail-rights"
                                    style="
                                      max-width: 100%;
                                      margin: auto;
                                      font-size: 12px;
                                      color: #999;
                                      text-align: center;
                                      line-height: 22px;
                                    "
                                  >
                                    <img
                                      border="0"
                                      src="https://baseframeapi.fineex.net/upload//UpLoadImg/gongzhonghao.jpg"
                                      style="
                                        width: 64px;
                                        height: 64px;
                                        margin: 0 auto;
                                      "
                                    />
                                    <br />
                                    关注公众号，掌握最新动态
                                    <br />
                                    <p style="text-align: center;font-size: small;color: #c3c3c3;">
                                        © 2006-2023 上海发网供应链管理有限公司
                                    </p>
                                    <p style="text-align: center;font-size: small;color: #c3c3c3;">
                                        All Rights Reserved. 发网科技 版权所有
                                    </p>
                                  </p>
                                </td>
                                <td style="width: 3.2%; max-width: 30px"></td>
                              </tr>
                            </tbody>
                          </table>
                        </div>
                      </td>
                      <td style="width: 3%; max-width: 30px"></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </span>
        </div>
      </div>
    </div>
  </includetail>
</div>
        """
        return template

    def sendMail(self):
        """
        发送邮件
        :return:
        """
        if not self.msg['To']:
            raise "没有收件人,请先设置邮件基本信息"
        self.mailServer.sendmail(self.mailUser, self.msg['To'], self.msg.as_string())


    def getAttachmentFromFile(self, attachmentFilePath):
        """
        通过路径添加附件
        :param attachmentFilePath:
        :return:
        """
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(attachmentFilePath, "rb").read())
        encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % str(Header(os.path.basename(attachmentFilePath), 'utf8')))
        return part


if __name__ == "__main__":
    # 普通文本邮件
    sml1 = MailSender('liuchunyang@fineex.com', 'yourpassword', 'smtp.qiye.163.com:465')
    sml1.setMailInfo('993492649@qq.com', '测试标题', '测试正文', 'plain')
    sml1.sendMail()

    # html文件带文件
    sml2 = MailSender('liuchunyang@fineex.com', 'yourpassword', 'smtp.qiye.163.com:465')
    content = sml2.generateHtml('告警', '测试告警标题', '刘春阳', '测试告警内容')
    sml2.setMailInfo('993492649@qq.com', '测试标题', content, 'html', r'C:\Users\liuchunyang\Desktop\dist\dist.rar')
    sml2.sendMail()
