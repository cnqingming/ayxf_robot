import lark_oapi as lark
from lark_oapi.adapter.flask import *
from lark_oapi.api.im.v1 import *

from flask import Flask, request, jsonify, json

app = Flask(__name__)


def do_p2_im_message_receive_v1(data: P2ImMessageReceiveV1) -> None:
    ctt = json.loads(data.event.message.content)  # 要把数据转成json
    text = ctt['text']  # 从json字典里面吧key为text的值取出来

    user = data.event.sender.sender_id.open_id
    send_text(text, user)  # 传入text变量，user变量


def do_customized_event(data: lark.CustomizedEvent) -> None:
    print(lark.JSON.marshal(data))


def send_text(text, user):
    # 创建client，id and secret都是机器人的
    client = lark.Client.builder() \
        .app_id("cli_a5f0588fee7a9013") \
        .app_secret("pcn3sT4IlA4OwFICXAV6sc7EglUiigHq") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象 传入的receive_id_type要和自己的对应
    request: CreateMessageRequest = CreateMessageRequest.builder() \
        .receive_id_type("open_id") \
        .request_body(CreateMessageRequestBody.builder()
                      .receive_id(user)
                      .msg_type("text")
                      .content("{\"text\":\""+text+"\"}")
                      .build()) \
        .build()

    # 发起请求
    response: CreateMessageResponse = client.im.v1.message.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.message.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


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


if __name__ == '__main__':
    app.run(debug=True)
