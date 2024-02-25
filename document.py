import lark_oapi as lark  # import是倒入外部库
import lark_oapi.api.wiki.v2 as wiki_v2
import lark_oapi.api.im.v1 as im_v1
from flask import json
from lark_oapi.api.application.v6 import P2ApplicationBotMenuV6

from my_creator import LarkClientCreator


# 所有的业务逻辑都堆在了app.py里，要把函数挪进document里
# 理想情况是可以根据发送的命令到不同的逻辑分支
def do_p2_im_message_receive_v1(data: im_v1.P2ImMessageReceiveV1) -> None:
    ctt = json.loads(data.event.message.content)  # 要把数据转成json
    text = ctt['text']  # 从json字典里面吧key为text的值取出来

    user = data.event.sender.sender_id.open_id
    client = LarkClientCreator(  # 创建client，id and secret都是机器人的
        app_id="cli_a5f0588fee7a9013",
        app_secret="pcn3sT4IlA4OwFICXAV6sc7EglUiigHq"
    ).create_client()

    if text == "测试":  # 发送测试即可返回相同内容
        send_text(text, user, client)  # 传入text变量，user变量，将接收到的消息复读一遍发送
    elif text == "查询知识库列表":  # 添加了新的逻辑分支
        for name in list_space_request(client):  # 遍历list_space_request(client)的列表
            send_text(text=name, user=user, client=client)  # 调用text，user，client


#  我们目前的是只回复消息，后续也要处理菜单的命令，降低使用门槛
def do_boot_menu_event(data:P2ApplicationBotMenuV6) -> None:
     # print(lark.JSON.marshal(data))
    # 试着用一下飞书提供的接口吧少女！
    event_name = data.event.event_key

    user = data.event.operator.operator_id.open_id
    client = LarkClientCreator(  # 创建client，id and secret都是机器人的
        app_id="cli_a5f0588fee7a9013",
        app_secret="pcn3sT4IlA4OwFICXAV6sc7EglUiigHq"
    ).create_client()

    if event_name == '测试':
        send_text(event_name, user, client)
    # elif event_name == "帮助"
def list_space_request(client: lark.Client):
    # 构造请求对象
    request: wiki_v2.ListSpaceRequest = wiki_v2.ListSpaceRequest.builder() \
        .build()

    # 发起请求
    response: wiki_v2.ListSpaceResponse = client.wiki.v2.space.list(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.wiki.v2.space.list failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

    result = []  # 创建一个result的空列表

    for item in response.data.items:  # 遍历 response.data.items
        name_text = item.name
        result.append(name_text)  # 将name_text的值添加到result

    return result


def send_text(text, user, client: lark.Client):
    # 构造请求对象 传入的receive_id_type要和自己的对应
    request: im_v1.CreateMessageRequest = im_v1.CreateMessageRequest.builder() \
        .receive_id_type("open_id") \
        .request_body(im_v1.CreateMessageRequestBody.builder()
                      .receive_id(user)
                      .msg_type("text")
                      .content("{\"text\":\"" + text + "\"}")
                      .build()) \
        .build()

    # 发起请求
    response: im_v1.CreateMessageResponse = client.im.v1.message.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.message.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))
