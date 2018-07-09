from flask import Blueprint

# 创建蓝图对象
api = Blueprint("ai", __name__)

from . import testReview
