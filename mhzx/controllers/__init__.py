from .data import page_index

# 蓝本默认配置
DEFAULT_BLUEPRINT = (
    # (蓝本，前缀)
    (page_index, ''),
)


# 封装函数配置蓝本
def config_blueprint(app):
    for blueprint, url_prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=url_prefix)
