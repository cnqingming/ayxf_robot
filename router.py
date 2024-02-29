from datetime import datetime

import lark_oapi.api.im.v1 as im_v1
from flask import json
from lark_oapi.api.application.v6 import P2ApplicationBotMenuV6
from lark_client_functions import list_space_request, send_text, list_space_node, list_app_table, list_app_table_view, \
    search_table_record
from my_creator import LarkClientCreator


#  todo 将函数重构为Router类的能力，将client重构为该类的属性
def do_p2_im_message_receive_v1(data: im_v1.P2ImMessageReceiveV1) -> None:
    ctt = json.loads(data.event.message.content)  # 要把数据转成json
    text = ctt['text']  # 从json字典里面吧key为text的值取出来
    open_id = data.event.sender.sender_id.open_id
    client = LarkClientCreator(  # 创建client，id and secret都是机器人的
        app_id="cli_a5f0588fee7a9013",
        app_secret="pcn3sT4IlA4OwFICXAV6sc7EglUiigHq"
    ).create_client()
    router_message(client, text, open_id)


# 输入用户名和消息内容，根据消息内容路由执行相关逻辑
def router_message(client, text: str, open_id: str):
    if text == "测试":  # 发送测试即可返回相同内容
        send_text(text, open_id, client, "open_id")  # 传入text变量，open_id变量，将接收到的消息复读一遍发送
    elif text == "查询知识库列表":  # 添加了新的逻辑分支
        for name in list_space_request(client):  # 遍历list_space_request(client)的列表
            send_text(text=name, id=open_id, client=client, receive_id_type="open_id")  # 调用text，open_id，client
    elif "查询知识库已有文档" in text:  # text [查询知识库已有文档：爱与幸福文档整理]
        content = text.split("：")[1]  # ["查询知识库已有文档", "爱与幸福文档整理"]
        search_node_in_space(client=client, space_name=content, open_id=open_id)


def do_boot_menu_event(data: P2ApplicationBotMenuV6) -> None:
    # print(lark.JSON.marshal(data))
    # 试着用一下飞书提供的接口吧少女！
    event_name = data.event.event_key
    open_id = data.event.operator.operator_id.open_id
    client = LarkClientCreator(  # 创建client，id and secret都是机器人的
        app_id="cli_a5f0588fee7a9013",
        app_secret="pcn3sT4IlA4OwFICXAV6sc7EglUiigHq"
    ).create_client()
    router_event(client=client, open_id=open_id, event_name=event_name)


# 输入用户名和事件名，根据事件名路由执行相关逻辑
def router_event(client, open_id, event_name=None):
    # todo 可通过卡片进行逐步选择
    if event_name == '测试':
        send_text(event_name, open_id, client, "open_id")
    elif event_name == "查询已有文档":
        search_node_in_space(client=client, space_name="爱与幸福文档整理", open_id=open_id)
    elif "触发生日遍历" == event_name:
        trigger_birthday_judge(client=client, open_id=open_id)


def schedule_event():
    client = LarkClientCreator(  # 创建client，id and secret都是机器人的
        app_id="cli_a5f0588fee7a9013",
        app_secret="pcn3sT4IlA4OwFICXAV6sc7EglUiigHq"
    ).create_client()
    trigger_birthday_judge(client, "ou_4401ab37e37fb1f857c290fd4715e838")


def search_space_id(client, space_name, open_id):
    items = list_space_request(client)
    for item in items:
        if item.name == space_name:
            return item.space_id
    send_text(text=f"找不到知识库 '{space_name}' ", id=open_id, client=client, receive_id_type="open_id")
    return None


def search_node_token(client, space_id, node_name, open_id):
    nodes = list_space_node(space_id, client)
    for node in nodes:
        if node_name == node.title:
            return node
    send_text(text=f"找不到知识库节点 '{node_name}' ", id=open_id, client=client, receive_id_type="open_id")


def search_table(client, app_token, table_name, open_id):
    tables = list_app_table(app_token, client)
    for table in tables:
        if table_name == table.name:
            return table
    send_text(text=f"找不到数据表 '{table_name}' ", id=open_id, client=client, receive_id_type="open_id")


def search_table_view(client, app_token, table_id, table_view_name, open_id):
    views = list_app_table_view(app_token, table_id, client)
    for view in views:
        if table_view_name == view.view_name:
            return view
    send_text(text=f"找不到数据表视图 '{table_view_name}' ", id=open_id, client=client, receive_id_type="open_id")


def trigger_birthday_judge(client, open_id):
    # 遍历生日，发送提醒
    #  新入口，实现定时调用能力

    # 1. 定位到知识库 - 对应节点 - 对应多维表格 - 对应视图
    space_id = search_space_id(client=client, space_name="成长小组知识库", open_id=open_id)
    app_token = search_node_token(client=client, space_id=space_id, node_name="【新青年】管理表格", open_id=open_id).obj_token
    table_id = search_table(client=client, app_token=app_token, table_name="新青年活动事件总表", open_id=open_id).table_id
    view_id = search_table_view(client=client, app_token=app_token, table_id=table_id, table_view_name="总表",
                                open_id=open_id).view_id
    records = search_table_record(client=client, app_token=app_token, table_id=table_id, view_id=view_id)  # 2. 拿到所有记录，
    # 获取当前年份
    current_year = datetime.now().year
    # 获取今天的日期
    now = datetime.now()
    today_string = now.strftime("%Y-%m-%d")
    output_text = f"今日 {today_string}"
    # 3. 遍历所有记录的生日字段，和今天的日期做对比
    for record in records:
        date_string = record.fields.get("生日")
        if not date_string:
            continue
        timestamp = date_string["value"][0] / 1000
        name_string = record.fields.get("姓名")[0]["text"]
        date = datetime.fromtimestamp(timestamp)
        # 创建一个新的日期, 使用当前年份但月份和日期与原日期相同
        new_date = date.replace(year=current_year)
        new_date_string = new_date.strftime("%Y-%m-%d")
        years = current_year - date.year
        days_until = (new_date - now).days
        # 4. 保存生日在未来七天内记录，以【姓名 + 倒数天数】输出，发送消息
        if 0 <= days_until < 7:
            output_text += f"\\n{name_string}将在{days_until}天后的 {new_date_string} 迎来{years}岁生日"
    send_text(output_text, open_id, client, "open_id")
    send_text(output_text, "oc_d129a202480be6f268bbfffd373d4b45", client, receive_id_type="chat_id")


# 输入用户名和知识库名称，查询知识库，并发送知识库的文件内容
def search_node_in_space(client, space_name, open_id):
    # 1. 获取知识库列表，将名称为space_name的知识库数据捞出来，获取space_id
    space_id = search_space_id(
        client=client,
        space_name=space_name
    )
    # space_id 判空逻辑
    if space_id:
        # 2. 获取知识库内所有一级文档（查询知识库内文档）
        nodes = list_space_node(space_id, client)
        # 3. 将一级文档（标题+链接）以消息形式返回
        text = ""  # 现在text为空
        for node in nodes:  # 遍历node，传入title和url
            title = node.title + ":"
            url = "https://ti5z9w2m1c8.feishu.cn/wiki/" + node.node_token  # 飞书知识库文档的组成是前面的链接+node token
            text += title + url + "\\n"  # todo 为什么传"\\n"
        send_text(text, open_id, client, "open_id")  # 调用send text
    else:
        # 变量没有匹配时的兜底逻辑
        send_text(text=f"找不到知识库 '{space_name}' ", id=open_id, client=client, receive_id_type="open_id")
    # todo 梳理文档知识库常用命令：查询已有文档 / 生成新模版文档

# 输入space_name，如匹配，返回space_id，否则返回None

# todo 菜单功能【查询已有文档】
# 1. 获取知识库列表，将名称为“爱与幸福文档整理”的知识库数据捞出来，获取space_id
# 2. 获取知识库内所有一级文档（查询知识库内文档）
# 3. 将一级文档（标题+链接）以消息形式返回
# elif event_name == "触发生日遍历":
#     pass
