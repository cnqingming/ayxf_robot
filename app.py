import lark_oapi as lark
from lark_oapi.adapter.flask import *
from lark_oapi.api.im.v1 import *

from flask import Flask, request, jsonify, json

from document import send_text, list_space_request

app = Flask(__name__)


def do_p2_im_message_receive_v1(data: P2ImMessageReceiveV1) -> None:
    ctt = json.loads(data.event.message.content)  # 要把数据转成json
    text = ctt['text']  # 从json字典里面吧key为text的值取出来

    user = data.event.sender.sender_id.open_id
    client = LarkClientCreator(  # 创建client，id and secret都是机器人的
        app_id="cli_a5f0588fee7a9013",
        app_secret="pcn3sT4IlA4OwFICXAV6sc7EglUiigHq"
    ).create_client()

    send_text(text, user,client)  # 传入text变量，user变量，将接收到的消息复读一遍发送


    for name in list_space_request(client):
        send_text(text=name,user=user,client=client)


def do_customized_event(data: lark.CustomizedEvent) -> None:
    print(lark.JSON.marshal(data))


handler = lark.EventDispatcherHandler.builder("", "sIbA8tRAgaRNQo9MjKsZUbvYMTp1jXo0", lark.LogLevel.DEBUG) \
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1) \
    .register_p1_customized_event("message", do_customized_event) \
    .build()


@app.route('/')
def hello_world():
    return 'Hello, World! by Liz'


@app.route('/myEvent', methods=['POST'])
def feishu_webhook():
    # 解析请求数据
    data = request.get_json()

    # 检查请求类型
    if data.get('type') == 'url_verification':
        # 如果是验证请求，提取 challenge 并返回
        challenge = data.get('challenge')
        return jsonify({'challenge': challenge})

    # 对于其他类型的请求，可以添加相应的处理逻辑
    # ...

    resp = handler.do(parse_req())
    return parse_resp(resp)


class LarkClientCreator:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

    def create_client(self):
        # 在这里构建你的 lark.Client 实例
        client = lark.Client.builder() \
            .app_id(self.app_id) \
            .app_secret(self.app_secret) \
            .log_level(lark.LogLevel.DEBUG) \
            .build()
        return client


if __name__ == '__main__':
    app.run(debug=True)
