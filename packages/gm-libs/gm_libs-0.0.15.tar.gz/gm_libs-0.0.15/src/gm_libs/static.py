# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *
from gm_libs import log_all


# 计算近期净值变动率（3、6、12 月）
def l_static_month_rate(context):
    context.l_statics["nav"].append(context.account().cash.nav)
    if len(context.l_statics["nav"]) > 12:
        del context.l_statics["nav"][0]

    # 输出日志
    nav_len = len(context.l_statics["nav"])
    year_rate = 0
    half_year_rate = 0
    season_rate = 0
    if nav_len >= 12:
        year_rate = 1 - context.l_statics["nav"][nav_len - 1] / context.l_statics["nav"][nav_len - 12] * 100
    if nav_len >= 6:
        half_year_rate = 1 - context.l_statics["nav"][nav_len - 1] / context.l_statics["nav"][nav_len - 6] * 100
    if nav_len >= 3:
        season_rate = 1 - context.l_statics["nav"][nav_len - 1] / context.l_statics["nav"][nav_len - 3] * 100

    log_all("warn", "【基准收益】日期: %s | 12月: %.1f%% | 6月: %.1f%% | 3月: %.1f%%" % (
        context.today_str, year_rate, half_year_rate, season_rate), filetype="static")


# 按日计算回撤区间
def l_static_day_back(context):
    # todo 如果有回撤起点：相比昨日，今天跌，记录回撤起点（昨日净值）
    # todo 如果无回撤起点：相比昨日，今天涨，记录回撤日志，清理回撤起点
    pass

