from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import datetime


class SmsSender:
    """
    使用阿里云短信服务发送短信
    """
    def __init__(self, access_key_id, access_key_secret, sign_name, template_code):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.sign_name = sign_name
        self.template_code = template_code

    def sendSms(self, phone_number, **kwargs):
        acs_client = AcsClient(self.access_key_id, self.access_key_secret, self.template_code)

        request = CommonRequest()

        # 设置请求参数
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        # 设置API版本号
        print(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        request.set_version('2017-05-25')
        # 设置API操作名
        request.set_action_name('SendSms')

        # 设置短信模板参数
        request.add_query_param('PhoneNumbers', phone_number)
        request.add_query_param('SignName', self.sign_name)
        request.add_query_param('TemplateCode', self.template_code)

        # 模板参数
        request.add_query_param('TemplateParam', kwargs)

        # 发送短信请求并获取返回结果
        response = acs_client.do_action_with_exception(request)

        print(response)


if __name__ == '__main__':
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
