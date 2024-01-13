# coding=utf-8
from __future__ import print_function, absolute_import

from os import getcwd

from gm.api import *
import pymysql.cursors
from gm_libs import l_get_log_path, l_copy_file_to_log

# 数据库连接
l_db = None  # Connection[Cursor]
l_config = {}  # dict


# 运行初始化
def l_init_run(context, configs=None):
    global l_config
    if configs is None:
        configs = {
            "db": {
                'host': 'localhost',
                'user': 'root',
                'password': 'testPass',
                'database': 'stock',
                'charset': 'utf8mb4',
                'cursorclass': pymysql.cursors.DictCursor
            }
        }
    configs['mode'] = context.mode
    l_config = configs

    context.l_statics = {
        "month": 0,  # 昨日月份
        "nav": [],  # 获得收益
    }

    # 将代码快照保存一份
    print(getcwd())
    filename = "main.py"
    filepath = "%s/%s" % (getcwd(), filename)
    l_copy_file_to_log(filepath, filename)


# 每日初始化
def l_init_day(context):
    context.today_str = context.now.strftime("%Y-%m-%d")


# 获取一个数据库连接
def l_db_connect():
    global l_db
    global l_config
    if l_db is None or l_db.open is False:
        l_db = pymysql.connect(host=l_config['host'],
                               user=l_config['user'],
                               password=l_config['password'],
                               database=l_config['database'],
                               charset=l_config['charset'],
                               cursorclass=l_config['cursorclass'])
    return l_db


# 结束输出
def l_finished(context):
    print("回测完成，请前往", l_get_log_path(), "查看相关日志。")
