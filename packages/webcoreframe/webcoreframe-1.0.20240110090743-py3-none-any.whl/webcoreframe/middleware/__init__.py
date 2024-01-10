from flask import Flask

from webcoreframe.middleware.authentication import Authentication
from webcoreframe.middleware.authorization import Authorization
from webcoreframe.middleware.blacklist import SysIPBlackList
from webcoreframe.middleware.blacklist import SysUserBlackList
from webcoreframe.middleware.performance_check import Performance
from webcoreframe.middleware.request_args import RequestArgs
from webcoreframe.middleware.request_filters import RequestFilters
from webcoreframe.middleware.request_keys import RequestKeys
from webcoreframe.middleware.response import ResponseEncrypt
from webcoreframe.middleware.system import SystemLogging
from webcoreframe.plugins.limiter_helper import init_limiter


def init_middleware(app: Flask):
    from webcoreframe.utils.helper import load_model
    middlewares = app.config.get("WEBCOREFRAME_MIDDLEWARE")
    if not middlewares:
        return
    for middleware in middlewares:
        m = load_model(middleware)
        m(app)


__all__ = (
    "ResponseEncrypt",  # 响应加密
    "Authentication",  # 认证
    "SystemLogging",  # 系统日志
    "SysIPBlackList",  # 系统IP黑名单
    "SysUserBlackList",  # 系统用户黑名单
    "RequestKeys",  # 参数解码
    "RequestArgs",  # 参数值解码
    "RequestFilters",  # 接口过滤
    "Authorization",  # 授权
    "init_limiter",  # 限流
    "Performance",  # 慢日志
    "init_middleware",
)
