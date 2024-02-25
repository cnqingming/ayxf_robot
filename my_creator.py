import lark_oapi as lark
class LarkClientCreator:  # 构造一个LarkClientCreator类
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

    def create_client(self):  # 创建lark.Client实例
        # 在这里构建你的 lark.Client 实例
        client = lark.Client.builder() \
            .app_id(self.app_id) \
            .app_secret(self.app_secret) \
            .log_level(lark.LogLevel.DEBUG) \
            .build()
        return client