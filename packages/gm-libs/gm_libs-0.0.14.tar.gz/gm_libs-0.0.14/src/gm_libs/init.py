# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *


# 运行初始化
def l_init_run(context):
    context.l_statics = {
        "month": 0,  # 昨日月份
        "nav": [],  # 获得收益
    }


# 每日初始化
def l_init_day(context):
    context.today_str = context.now.strftime("%Y-%m-%d")