import lark_oapi as lark
from lark_oapi.adapter.flask import *
from lark_oapi.api.im.v1 import *

from flask import Flask, request, jsonify, json

from document import send_text, list_space_request, do_p2_im_message_receive_v1, do_customized_event

app = Flask(__name__)






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
