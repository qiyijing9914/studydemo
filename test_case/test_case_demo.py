import random
from tools.api import request_tool
from tools.data.time_tool import get_now, get_today

# 创建一个公共字典，字典里边存放要存入的数据
d={}

# 上报案件
def test_report_message(pub_data):
    method = "POST"  # 请求方法，全部大写
    feature = "案件发现"  # allure报告中一级分类
    story = '待受理'  # allure报告中二级分类
    title = "案件上报"  # allure报告中用例名字
    uri = f"/api/web/events/report-message?id=false&token={pub_data['token']}"  # 接口地址
    status_code = 200  # 响应状态码
    expect = ""  # 预期结果
    data = {
        'reportContent': '{"city":"上海","district":5,"eventName":"住宅小区里废弃非机动车辆","eventDescription":"案件描述","street":"501","source":"1","degree":"","community":null,"address":"详细地址1","grid_center":"505001","audios":[],"videos":[],"scenes":[],"result":[],"areaType":"1","eventType":{"level_1":"事件","level_2":"市容环卫","level_3":"废弃车辆"},"lngCd":0,"latCd":0}',
        'handleChannel': '3',
        'type': '1'}
    # --------------------分界线，下边的不要修改-----------------------------------------
    # method,pub_data和url为必传字段
    r = request_tool.request(method=method, url=uri, pub_data=pub_data, status_code=status_code,
                             expect=expect, feature=feature, story=story, title=title, data=data)
    assert r.json()["code"] == 200 and r.json()["data"] == True
# 街道案件受理
def test_accept_and_hear_a_case(pub_data,db):
    # 前置操作,查询数据库数据获取案件的eventId
    # mysql = mysql_db('172.16.25.52', 'paidan_user', 'aaA5y6C9vL', 'test2')
    # 查询当天指定用户id上传的案件编号
    query_data = db.select_execute(
        f"SELECT event_id FROM `test2`.`event` WHERE created_at LIKE '{get_today()}%' and cuser='1862'  ORDER BY code DESC LIMIT 1;")
    d["eventId"] = random.choice(query_data)[0]
    method = "PATCH"  # 请求方法，全部大写
    feature = "案件发现"  # allure报告中一级分类
    story = '待受理'  # allure报告中二级分类
    title = "受理"  # allure报告中用例名字
    uri = f"/api/web/events/{d['eventId']}?token={pub_data['token']}&id={d['eventId']} "  # 接口地址
    headers = {"Content-Type": "application/json;charset=utf-8"}
    status_code = 200  # 响应状态码
    expect = ""  # 预期结果
    data = {"data": {"status": "12", "desc": "同意受理！", "withNext": 0, "nextDesc": ""}}
    # --------------------分界线，下边的不要修改-----------------------------------------
    # method,pub_data和url为必传字段
    r = request_tool.request(method=method, url=uri, pub_data=pub_data, status_code=status_code, headers=headers,
                             expect=expect, feature=feature, story=story, title=title, json_data=data)
    d["code"] = r.json()["data"]["code"]
    print("案件编号:" + d["code"])
    print("案件编号:" + d["eventId"])
    assert r.json()["code"] == 200 and r.json()["data"] != None
# 街道案件立案
def test_the_case_file(pub_data):
    method = "PUT"  # 请求方法，全部大写
    feature = "案件立案"  # allure报告中一级分类
    story = '待立案'  # allure报告中二级分类
    title = "立案"  # allure报告中用例名字
    uri = f"/api/web/events/{d['eventId']}?token={pub_data['token']}&id={d['eventId']}"  # 接口地址
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    status_code = 200  # 响应状态码
    expect = ""  # 预期结果
    json_data = '''{"data":{"eventName":"住宅小区里废弃非机动车辆","address":"详细地址1","eventDescription":"案件描述","eventType":{"level_1":"事件","level_2":"市容环卫","level_3":"废弃车辆"},"community":"","source":1,"images":[],"status":13,"confirm_info":{"description":"案件情况属实，予以立案，请派遣处置！"}}}'''
    # --------------------分界线，下边的不要修改-----------------------------------------
    # method,pub_data和url为必传字段
    r = request_tool.request(method=method, url=uri, pub_data=pub_data, status_code=status_code, headers=headers,
                             expect=expect, feature=feature, story=story, title=title, json_data=json_data)
    assert r.json()["code"] == 200 and r.json()["data"] != None
# 向下派遣
def test_dispatch_meta(pub_data):
    # 前置操作.根据指定的eventId获取指定的id实现动态参数化

    method = "POST"  # 请求方法，全部大写
    feature = "案件派遣"  #  allure报告中一级分类
    story = '待派遣'  # allure报告中二级分类
    title = "向下派遣(部门)"  # allure报告中用例名字
    print("向下派遣的案件编号:" + d["eventId"])
    uri = f"/api/web/case/dispatch-meta?id={d['eventId']}&token={pub_data['token']}"  # 接口地址
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    status_code = 200  # 响应状态码
    expect = ""  # 预期结果
    data = {'id': '665031', 'meta_id': '501012','deps':[],'deal':f'{get_now()}','desc':'请尽快进行处理，并在处理完成后及时反馈。'}
    # --------------------分界线，下边的不要修改-----------------------------------------
    # method,pub_data和url为必传字段
    r = request_tool.request(method=method, url=uri, pub_data=pub_data, status_code=status_code, headers=headers,
                             expect=expect, feature=feature, story=story, title=title, json_data=data)
    assert r.json()["code"] == 200 and r.json()["data"] == True