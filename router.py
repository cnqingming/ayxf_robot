import lark_oapi.api.im.v1 as im_v1
from flask import json
from lark_oapi.api.application.v6 import P2ApplicationBotMenuV6
from lark_client_functions import list_space_request, send_text, list_space_node
from my_creator import LarkClientCreator


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


def do_boot_menu_event(data: P2ApplicationBotMenuV6) -> None:
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
    elif event_name == "查询已有文档":
        # 1. 获取知识库列表，将名称为“爱与幸福文档整理”的知识库数据捞出来，获取space_id
        items = list_space_request(client)
        for item in items:
            if item.name == "爱与幸福文档整理":
                space_id = item.space_id
            else:
                continue
        # 2. 获取知识库内所有一级文档（查询知识库内文档）
        nodes = list_space_node(space_id, client)
        # 3. 将一级文档（标题+链接）以消息形式返回
        text = ""  # 现在text为空
        for node in nodes:  # 遍历node，传入title和url
            title = node.title + ":"
            url = "https://ti5z9w2m1c8.feishu.cn/wiki/" + node.node_token  # 飞书知识库文档的组成是前面的链接+node token
            text += title + url + "\\n" # todo 为什么传"\\n"
        send_text(text, user, client)  # 调用send text


    # todo 梳理文档知识库常用命令：查询已有文档 / 生成新模版文档

    # todo 菜单功能【查询已有文档】
    # 1. 获取知识库列表，将名称为“爱与幸福文档整理”的知识库数据捞出来，获取space_id
    # 2. 获取知识库内所有一级文档（查询知识库内文档）
    # 3. 将一级文档（标题+链接）以消息形式返回
