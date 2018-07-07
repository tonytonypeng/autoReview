import redis

class Config(object):
    """工程的配置信息"""

    # redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

class DevelopmentConfig(Config):
    """开发模式使用的配置信息"""
    DEBUG = True

class ProductionConfig(Config):
    """生产模式 线上模式的配置信息"""
    pass

config_dict = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}