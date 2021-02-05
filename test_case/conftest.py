import random

import pytest

from config.conf import PAIDAN_DB_QA
from tools.api import request_tool
from tools.data.mysql_tool import mysql_db
from tools.data.time_tool import get_today


# 获取登录的token
def paidan_login():
    method = "POST"  # 请求方法，全部大写
    feature = "用户模块"  # allure报告中一级分类
    story = '用户登录'  # allure报告中二级分类
    title = "登录"  # allure报告中用例名字
    uri = "/api/app/users/login"  # 接口地址
    headers = {'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json;charset=UTF-8'}
    status_code = 200  # 响应状态码
    expect = ""  # 预期结果
    # json_data = """{"username":%s,"password":%s}"""%(username,password)
    json_data = {"username": "jdadmin", "password": "123456"}
    # --------------------分界线，下边的不要修改-----------------------------------------
    # method,pub_data和url为必传字段
    r = request_tool.request(method=method, url=uri, pub_data=pub_data, status_code=status_code, headers=headers,
                             expect=expect, feature=feature, story=story, title=title, json_data=json_data)
    return r.json()["data"]["token"]


# 获取数据库中指定用户的案件加密编号
def query_case_code():
    mysql = mysql_db('172.16.25.52', 'paidan_user', 'aaA5y6C9vL', 'test2')  #
    # 查询当天+指定用户id上传的案件编号
    query_data = mysql.select_execute(
        f"SELECT event_id FROM `test2`.`event` WHERE created_at LIKE '{get_today()}%' and cuser='1862'  ORDER BY code DESC LIMIT 1;")
    case_code = random.choice(query_data)[0]
    return case_code


# 将获取的token和案件编号返回给调用者
@pytest.fixture(scope='session')
def pub_data():
    data = {'token': paidan_login()}  # , 'case_code': query_case_code()
    return data

# @pytest.fixture(scope='session')
# def db():
#     mysql = mysql_db('172.16.25.52', 'paidan_user', 'aaA5y6C9vL', 'test2')
#     query_data = mysql.select_execute(
#         f"SELECT event_id FROM `test2`.`event` WHERE created_at LIKE '{get_today()}%' and cuser='1862'  ORDER BY code DESC LIMIT 1;")
#     print(random.choice(query_data)[0])
#     data = {'case_code': random.choice(query_data)[0]}
#     return data

@pytest.fixture(scope='session')
def db():
    return mysql_db(**PAIDAN_DB_QA)
