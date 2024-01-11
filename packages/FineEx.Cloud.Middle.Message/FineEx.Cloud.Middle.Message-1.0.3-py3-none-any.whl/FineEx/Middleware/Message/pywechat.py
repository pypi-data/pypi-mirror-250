import sys
import time
import hashlib
from pathlib import Path
import configparser
import requests
from typing import Optional, Union
import logging

chat_api = {
    'GET_ACCESS_TOKEN': '/cgi-bin/gettoken?corpid={}&corpsecret={}',
    'MESSAGE_SEND': '/cgi-bin/message/send?access_token={}',
    'MEDIA_UPLOAD': '/cgi-bin/media/upload?access_token={}&type={}',
    "IMG_UPLOAD": '/cgi-bin/media/uploadimg?access_token={}',
    "GET_USERS": "/cgi-bin/user/simplelist"
}


class WorkChatSender:
    def __init__(self, corpid: Optional[str] = None, corpsecret: Optional[str] = None, agentid: Optional[int] = None):
        """
        构造函数
        :param corpid: 公司ID
        :param corpsecret: 密钥
        :param agentid: 应用ID
        :return:
        """
        self._Handler = HandlerTool(corpid, corpsecret, agentid)

    def get_token(self):
        """
        获取token
        :return: token
        """
        return self._Handler.get_token()

    def send_text(self, message, **kwargs):
        """
        发送文本消息，支持换行、以及A标签，大小最长不超过2048字节
        :param message:  消息内容
        :param kwargs:  可选择发送对象，tousers(用户), todept(部门), totags(标签用户). 默认为发送全部人
        """
        text_msg = {"content": message}
        self._Handler.send_message("text", text_msg, **kwargs)

    def send_markdown(self, markdown, **kwargs):
        """
        发送Markdown消息
        :param markdown: markdown内容
        :param kwargs: 可选择发送对象，tousers(用户), todept(部门), totags(标签用户). 默认为发送全部人
        """
        markdown_msg = {"content": markdown}
        self._Handler.send_message("markdown", markdown_msg, **kwargs)

    def send_image(self, iamge_path, **kwargs):
        """
        发送图片消息，仅支持jpg,png格式，大小5B~2M
        :param iamge_path: 发送图片的本地路径
        :param kwargs: 可选择发送对象，tousers(用户), todept(部门), totags(标签用户).
        """
        image_msg = {"media_id": iamge_path}
        self._Handler.send_message("image", image_msg, **kwargs)

    def send_voice(self, voice_path, **kwargs):
        """
        发送语音消息，仅支持amr格式，大小5B~2M
        :param voice_path: 发送语音文件的本地路径
        :param kwargs: 可选择发送对象，tousers(用户), todept(部门), totags(标签用户).
        :return:
        """
        voice_msg = {"media_id": voice_path}
        self._Handler.send_message("voice", voice_msg, **kwargs)

    def send_video(self, video_path, title=None, desc=None, **kwargs):
        """
        发送视频消息，仅支持MP4格式的视频消息，大小5B~10M
        :param video_path: 发送视频文件的本地路径
        :param title: 视频消息的标题，不超过128个字节，超过会自动截断.当不指定时默认为上传视频的文件名
        :param desc: 视频消息的描述，不超过512个字节，超过会自动截断
        :param kwargs: 可选择发送对象，tousers(用户), todept(部门), totags(标签用户).
        :return:
        """
        video_msg = {"media_id": video_path}

        if title:
            video_msg["title"] = title

        if desc:
            video_msg["description"] = desc

        self._Handler.send_message("video", video_msg, **kwargs)

    def send_file(self, file_path, **kwargs):
        """
        发送文件消息, 大小5B~10M
        :param file_path: 发送文件的本地路径
        :param kwargs: tousers(用户), todept(部门), totags(标签用户).
        :return:
        """
        file_msg = {"media_id": file_path}
        self._Handler.send_message("file", file_msg, **kwargs)

    def send_textcard(self, card_title, desc, link, btn="详情", **kwargs):
        """
        发送文本卡片消息
        :param card_title: 标题，不超过128个字节，超过会自动截断
        :param desc: 描述，不超过512个字节，超过会自动截断
        :param link: 点击后跳转的链接。最长2048字节，请确保包含了协议头(http/https)
        :param btn: 按钮文字。 默认为“详情”， 不超过4个文字，超过自动截断。
        :param kwargs: tousers(用户), todept(部门), totags(标签用户).
        :return:
        """
        textcard_msg = {
            "title": card_title,
            "description": desc,
            "url": link,
            "btntxt": btn
        }
        self._Handler.send_message("textcard", textcard_msg, **kwargs)

    def send_graphic(self, card_title, desc, link, image_link, **kwargs):
        """
        发送图文卡片消息
        :param card_title: 卡片标题
        :param desc:  卡片描述
        :param link:  点击后跳转的链接
        :param image_link: 图片url
        :param kwargs: tousers(用户), todept(部门), totags(标签用户).
        :return:
        """
        graphic_msg = {"articles": [{
            "title": card_title,
            "description": desc,
            "url": link,
            "picurl": image_link
        }]}
        self._Handler.send_message("news", graphic_msg, **kwargs)

    def upload_image(self, image_path, enable=True):
        """
        上传图片，返回图片链接，永久有效，主要用于图文消息卡片. imag_link参数
        图片大小：图片文件大小应在 5B ~ 2MB 之间
        :param image_path:  图片路径
        :param enable:  是否开启记录上传图片返回的url,会在当前文件夹下创建一个imagesList.txt.置为False 不持久化，默认True
        :return: 图片链接，永久有效
        """
        image_url = self._Handler.upload_image(image_path, enable=enable)
        return image_url

    def get_users_id(self, department_id=1, fetch_child=0):
        """
        通过部门ID查询部门下的员工
        :param department_id: 部门ID,默认根部门ID为1
        :param fetch_child:  是否递归查询子部门员工
        :return: 会显示所有的员工信息，主要用于查询对应用户的userid进行发送
        """
        params = {"department_id": department_id, "fetch_child": fetch_child}
        self._Handler.get_users_id(params)


class HandlerTool:
    """
    处理类
    """

    def __init__(self, corpid=None, corpsecret=None, agentid=None):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self._op = None
        self.url = 'https://qyapi.weixin.qq.com'
        self.conf = configparser.ConfigParser()
        self.token = self.get_token()

    @staticmethod
    def is_image(file):

        if not (file.suffix in (".JPG", ".PNG", ".jpg", ".png") and (5 <= file.stat().st_size <= 2 * 1024 * 1024)):
            raise TypeError(
                {"Code": "ERROR", "message": '图片文件不合法, 请检查文件类型(jpg, png, JPG, PNG)或文件大小(5B~2M)'})

    @staticmethod
    def is_voice(file):

        if not (file.suffix in (".AMR", ".amr") and (5 <= file.stat().st_size <= 2 * 1024 * 1024)):
            raise TypeError({"Code": "ERROR", "message": '语音文件不合法, 请检查文件类型(AMR, amr)或文件大小(5B~2M)'})

    @staticmethod
    def is_video(file):

        if not (file.suffix in (".MP4", ".mp4") and (5 <= file.stat().st_size <= 10 * 1024 * 1024)):
            raise TypeError({"Code": "ERROR", "message": '视频文件不合法, 请检查文件类型(MP4, mp4)或文件大小(5B~10M)'})

    @staticmethod
    def is_file(file):
        if not (file.is_file() and (5 <= file.stat().st_size <= 10 * 1024 * 1024)):
            raise TypeError({"Code": "ERROR", "message": '普通文件不合法, 请检查文件类型或文件大小(5B~10M)'})

    def file_check(self, file_type, path):
        """
        验证上传文件是否符合标准
        :param file_type: 文件类型(image,voice,video,file)
        :param path:
        :return:
        """

        p = Path(path)
        filetypes = {"image": self.is_image, "voice": self.is_voice, "video": self.is_video, "file": self.is_file}

        chack_type = filetypes.get(file_type, None)

        if not chack_type:
            raise TypeError({"Code": 'ERROR', "message": '不支持的文件类型，请检查文件类型(image,voice,video,file)'})

        chack_type(p)
        return {"file": (p.name, p.read_bytes())}

    def _get(self, uri, **kwargs):
        """
        发起get请求
        :param uri: 需要请求的Url
        :param kwargs: 需要带入的参数
        :return:
        """

        try:
            rsp = requests.get(self.url + uri, **kwargs)
            rsp.raise_for_status()
            result = rsp.json()
            if result.get("errcode") == 0:
                return result

            elif result.get("errcode") == 40013 or result.get("errcode") == 40001:
                raise ValueError({"Code": result.get("errcode"), "message": "输入的corpid 或 corpsecret错误请检查"})

        except requests.RequestException as e:
            return e

    def _post(self, uri, **kwargs):
        """
        发起Post请求
        :param uri: 需要请求的Url
        :param kwargs: 请求所需的参数
        :return:
        """
        try:
            url = self.url + uri
            for i in range(2):
                rsp = requests.post(url.format(self.token), **kwargs)
                rsp.raise_for_status()
                result = rsp.json()

                if result.get("errcode") == 0:
                    return result

                elif result.get("errcode") == 42001 or result.get("errcode") == 40014:
                    logging.info('token失效，重新获取')
                    self.token = self._get_token()

                else:
                    logging.warning(f'消息发送失败！原因:{rsp.text}')
                    sys.exit()

        except requests.exceptions.HTTPError as HTTPError:
            raise requests.exceptions.HTTPError(
                f"发送失败， HTTP error:{HTTPError.response.status_code} , 原因: {HTTPError.response.reason}")

        except requests.exceptions.ConnectionError:
            raise requests.exceptions.ConnectionError("发送失败，HTTP connection error!")

        except requests.exceptions.Timeout:
            raise requests.exceptions.Timeout("发送失败，Timeout error!")

        except requests.exceptions.RequestException:
            raise requests.exceptions.RequestException("发送失败, Request Exception!")

    def get_token(self):
        """
        获取token
        :return:
        """

        # 先读文件如果没有就发起请求并写入文件返回，有就判断timeout失效就发起请求并写入文件返回，时效正常直接返回
        self._op = hashlib.md5(bytes(self.corpsecret + self.corpid, encoding='utf-8')).hexdigest()
        return self._get_token()

    def _get_token(self):

        tokenurl = chat_api.get("GET_ACCESS_TOKEN").format(self.corpid, self.corpsecret)
        rsp = self._get(tokenurl)
        tokeninfo = {"token": rsp.get("access_token"), "tokenout": str(int(time.time()) + rsp.get("expires_in"))}
        self.conf[self._op] = tokeninfo
        return rsp.get("access_token")

    def send_message(self, message_type, message, touser=None, todept=None, totags=None):
        """
        发送消息的主要接口封装和发起请求
        :param message_type: 发送消息的类型
        :param message: 发送消息的内容
        :param touser: 发送到具体的用户，当此参数为@all时，忽略todept,totags 参数并发送到全部人，此参数默认为@all
        用户名用 | 拼接。最多支持100个
        :param todept: 发送到部门，当tousers为默认@all 此参数会被忽略.部门之间用 | 拼接。最多支持100个
        :param totags: 发送到标签的用用户,当tousers为默认@all 此参数会被忽略. 标签之间用 | 拼接.最多支持100个
        :return:
        """
        data = {
            "msgtype": message_type,
            "agentid": self.agentid,
            message_type: message
        }

        if not (touser or todept or totags):
            data["touser"] = "@all"

        else:
            if touser:
                data["touser"] = touser

            if todept:
                data["toparty"] = todept

            if totags:
                data["totag"] = totags

        # 判断是否需要上传
        if message_type in ("image", "voice", "video", "file"):
            filepath = message.get("media_id")

            media_id = self.upload_media(message_type, filepath)
            message["media_id"] = media_id

        self._post(chat_api.get('MESSAGE_SEND'), json=data)
        logging.info(f"发送 {message_type} 消息成功...")

    def upload_media(self, file_type, path):
        """
        上传临时素材， 3天有效期
        :param file_type: 文件类型
        :param path: 文件路径
        :return: media_id
        """

        fileinfo = self.file_check(file_type, path)
        rsp = self._post(chat_api.get("MEDIA_UPLOAD").format("{}", file_type), files=fileinfo)
        return rsp.get("media_id")

    def upload_image(self, picture_path, enable=True):
        """
        上传图片，返回图片url，url永久有效
        图片大小：图片文件大小应在 5B ~ 2MB 之间
        :param picture_path:  图片路径
        :param enable:  是否开启上传记录
        :return: 图片url，永久有效
        """

        p_imag = Path(picture_path)

        if not p_imag.is_file() or p_imag.stat().st_size > 2 * 1024 * 1024 or p_imag.stat().st_size <= 5:
            raise TypeError({"error": 'ERROR', "message": '指向的文件不是一个正常的图片或图片大小未在5B ~ 2MB之间',
                             "massage": f"{p_imag.name}: {p_imag.stat().st_size} B"})
        files = {"file": p_imag.read_bytes(), "filename": p_imag.name}

        rsp = self._post(chat_api.get("IMG_UPLOAD"), files=files)
        logging.info("图片上传成功...")
        if enable:
            with open('./imagesList.txt', "a+", encoding='utf-8') as fp:
                fp.write(f"{p_imag.name}: {rsp.get('url')}\n")

        return rsp.get("url")

    def get_users_id(self, data):
        data["access_token"] = self.token
        rsp_users = self._get(chat_api.get('GET_USERS'), params=data)
        for i in rsp_users.get("userlist"):
            logging.info(i)


if __name__ == '__main__':
    corpid = 'corpid'
    corpsecret = 'corpsecret'
    agentid = 'agentid'
    workSender = WorkChatSender(corpid=corpid, corpsecret=corpsecret, agentid=agentid)
    workSender.send_text("hello", touser='91237')
    subject = '测试异常'
    message = f"""
        >**测试信息异常** 
        请尽快处理！
        查看详情，请点击：[FineEx](https://www.fineex.com)
        """
    workSender.send_markdown(subject + "\n" + message.strip())
    workSender.send_image(r"iamge_path", touser='91237')
    workSender.send_file(r"file_path", touser='91237')
    workSender.send_video(r"video_path", touser='91237')
    workSender.send_voice(r"voice_path", touser='91237')