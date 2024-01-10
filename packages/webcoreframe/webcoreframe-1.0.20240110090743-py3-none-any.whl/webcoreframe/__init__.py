from flask import Flask


def init_app(app: Flask):
    from webcoreframe.application import init_models
    init_models(app)

    from webcoreframe.redis_helper.helper import init_redis_helper
    init_redis_helper(app)

    from webcoreframe.log.helper import init_logger
    init_logger(app)

    from webcoreframe.plugins.plugins import init_plugin
    init_plugin(app)

    from webcoreframe.middleware import init_middleware
    init_middleware(app)
