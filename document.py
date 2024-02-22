import lark_oapi as lark  # import是倒入外部库
import lark_oapi.api.wiki.v2 as wiki_v2
import lark_oapi.api.im.v1 as im_v1


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


    for item in  response.data.items:  # 遍历 response.data.items
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
