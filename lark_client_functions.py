import lark_oapi as lark
from lark_oapi.api.im import v1 as im_v1
from lark_oapi.api.wiki import v2 as wiki_v2
from lark_oapi.api.wiki.v2 import ListSpaceNodeRequest, ListSpaceNodeResponse


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

    # todo 目前只返回了知识库名称列表，后续应该将知识库信息打包，完整返回

    return response.data.items  # 简化调用items的逻辑


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


def list_space_node(space_id, client: lark.Client):  # 定义新的函数，获取知识空间子节点列表

    # 构造请求对象，根据技术文档需要传一个space_id
    request: ListSpaceNodeRequest = ListSpaceNodeRequest.builder() \
        .space_id(space_id) \
        .build()

    # 发起请求
    response: ListSpaceNodeResponse = client.wiki.v2.space_node.list(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.wiki.v2.space_node.list failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

    return response.data.items  # 对齐上面的items，直接调用
