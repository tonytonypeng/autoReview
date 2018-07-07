import logging
from config import config_dict
from flask import Flask
from logging.handlers import RotatingFileHandler
from pymongo import MongoClient
import redis

# mongodb
mongoClient = MongoClient()

# 构建redis连接对象
redisClient = None

# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)  # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*2, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日记录器
logging.getLogger().addHandler(file_log_handler)

# 工厂模式
def create_app(config_name):
    """创建flask应用对象"""
    app = Flask(__name__)

    conf = config_dict[config_name]

    # 设置flask的配置信息
    app.config.from_object(conf)

    # 初始化redis
    global redis_store
    redisClient = redis.StrictRedis(host=conf.REDIS_HOST, port=conf.REDIS_PORT)

    # 注册蓝图
    from ai import controller
    app.register_blueprint(controller.api, url_prefix="/api/v1_0")

    return app
