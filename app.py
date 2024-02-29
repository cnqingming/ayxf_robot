import lark_oapi as lark
from lark_oapi.adapter.flask import *
from flask import Flask, request, jsonify
from router import do_boot_menu_event, do_p2_im_message_receive_v1, schedule_event
from apscheduler.schedulers.background import BackgroundScheduler
import logging

app = Flask(__name__)
handler = lark.EventDispatcherHandler.builder("", "sIbA8tRAgaRNQo9MjKsZUbvYMTp1jXo0", lark.LogLevel.DEBUG) \
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1) \
    .register_p2_application_bot_menu_v6(do_boot_menu_event) \
    .build()


# .register_p1_customized_event("message", do_customized_event) \
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
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    # 创建后台调度器
    scheduler = BackgroundScheduler(daemon=True)
    # 设置调度器的时区为北京时间
    scheduler.configure(timezone="Asia/Shanghai")
    # 创建定时任务，触发时间在每日的12点执行
    scheduler.add_job(func=schedule_event, trigger="cron", hour=10, minute=0, second=0)
    scheduler.start()
    app.run(debug=True)
