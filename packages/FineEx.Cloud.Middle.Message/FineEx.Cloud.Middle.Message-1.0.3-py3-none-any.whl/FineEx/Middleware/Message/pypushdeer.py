import json
from typing import Optional, Union
import requests


class PushDeerSender:
    server = "https://api2.pushdeer.com"
    endpoint = "/message/push"
    pushkey = None

    def __init__(self, server: Optional[str] = None, pushkey: Optional[str] = None):
        if server:
            self.server = server
        if pushkey:
            self.pushkey = pushkey

    def _push(self, text: str, desp: Optional[str] = None, server: Optional[str] = None,
              pushkey: Optional[str] = None, text_type: Optional[str] = None, **kwargs):

        if not pushkey and not self.pushkey:
            raise ValueError("pushkey 不能为空")

        res = self._send_push_request(desp, pushkey or self.pushkey, server or self.server, text, text_type, **kwargs)
        if res["content"]["result"]:
            result = json.loads(res["content"]["result"][0])
            if result["success"] == "ok":
                return True
            else:
                return False
        else:
            return False

    def _send_push_request(self, desp, key, server, text, type, **kwargs):
        return requests.get(server + self.endpoint, params={
            "pushkey": key,
            "text": text,
            "type": type,
            "desp": desp,
        }, **kwargs).json()

    def send_text(self, text: str, desp: Optional[str] = None, server: Optional[str] = None,
                  pushkey: Union[str, list, None] = None, **kwargs):
        """
        发送文本信息
        @param text: 信息标题
        @param desp: 详细信息描述
        @param server: 服务地址
        @param pushkey: pushDeer 密钥
        @return: 成功（True）/失败（False）
        """
        return self._push(text=text, desp=desp, server=server, pushkey=pushkey, text_type='text', **kwargs)

    def send_markdown(self, text: str, desp: Optional[str] = None, server: Optional[str] = None,
                      pushkey: Union[str, list, None] = None, **kwargs):
        """
        发送Markdown信息
        @param text: 信息标题
        @param desp: 详细信息描述
        @param server: 服务地址
        @param pushkey: pushDeer 密钥
        @return: 成功（True）/失败（False）
        """
        return self._push(text=text, desp=desp, server=server, pushkey=pushkey, text_type='markdown', **kwargs)

    def send_image(self, image_src: str, desp: Optional[str] = None, server: Optional[str] = None,
                   pushkey: Union[str, list, None] = None, **kwargs):
        """
        发送图片信息
        @param image_src: 图片URL
        @param desp: 详细信息描述
        @param server: 服务地址
        @param pushkey: pushDeer 密钥
        @return: 成功（True）/失败（False）
        """
        return self._push(text=image_src, desp=desp, server=server, pushkey=pushkey, text_type='image', **kwargs)


if __name__ == "__main__":
    pushdeer = PushDeerSender(pushkey="yourkey")
    pushdeer.send_text("hello world", desp="optional description")
    pushdeer.send_markdown("# hello world", desp="**optional** description in markdown")
    pushdeer.send_image("https://github.com/easychen/pushdeer/raw/main/doc/image/clipcode.png")
    pushdeer.send_image("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVQYV2NgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII=")
