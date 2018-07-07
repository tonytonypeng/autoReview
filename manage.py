# coding:utf-8
from flask_script import Manager
from ai import create_app

# 创建flask的app
app = create_app("develop")

# 创建管理工具对象
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
