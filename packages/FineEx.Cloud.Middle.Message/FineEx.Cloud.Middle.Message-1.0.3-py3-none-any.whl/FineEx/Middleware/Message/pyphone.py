# -*- coding:utf-8 -*-
import requests
import urllib


class PhoneCaller:
    def __init__(self, account, password):
        self.account = account
        self.password = password
        self.url = "http://api.vm.ihuyi.com/webservice/voice.php?method=Submit"

    def call(self, text, mobile):
        """
        语音播报
        :param text: 播报内容，需要符合已授权模板，https://user.ihuyi.com/new/vm/send/template
        :param mobile: 电话号
        :return:
        """
        params = urllib.parse.urlencode(
            {'account': self.account, 'password': self.password, 'content': text, 'mobile': mobile, 'format': 'json'})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        response = requests.post(url=self.url, params=params, headers=headers)
        response_str = response.read()
        return response_str


if __name__ == '__main__':
    caller = PhoneCaller('account', 'password')
    msg = '机房温度异常：嘉合机房当前温度30度，请尽快安排人员排查情况'
    mobile = '17601234567'
    print(caller.call(msg, mobile))
