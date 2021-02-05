#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import re


def list_to_dict(headers):
    d = {}
    for h in headers:
        if(h[:h.find(": ")].strip() in ["Content-Length","Host","Connection","accept","User-Agent","Content-Type","Origin","Referer","Accept-Encoding","Cookie","Accept-Language"]):
            continue
        d[h[:h.find(": ")].strip()] = h[h.find(": ")+1:].strip()
    return d

def str_to_dic(data):
    d = {}
    dl = data.split("&")
    for i in dl:
        d[i.split("=")[0]]=i.split("=")[1]
    return d


def make_code():

    with open("demo.txt","r") as f:
        content = f.read()


    request_line = content.split("\n\n")[0]
    request_headers = request_line.split('\n')[1:]
    request_line = request_line.split('\n')[0]
    request_content = content.split("\n\n")[1]
    r = {}
    method = request_line.split(" ")[0].strip()
    url = request_line.split(" ")[1].strip().split("://")[1].strip()
    uri = url[url.find('/'):]
    data=""
    if "?" in uri:
        data = uri[uri.find('?') + 1:]
        uri = uri[:uri.find('?')]
    headers = list_to_dict(request_headers)
    r["func_name"] = uri[uri.rfind("/")+1:]
    r["method"]=method
    r["uri"] = uri
    r["headers"] = headers

    req = '''def test_{func_name}(pub_data):
    method = "{method}"  #请求方法，全部大写
    feature = "用户模块"  # allure报告中一级分类
    story = '用户登录'  # allure报告中二级分类
    title = "全字段正常流_1"  # allure报告中用例名字
    uri = "{uri}"  # 接口地址
    headers = {headers}
    status_code = 200  # 响应状态码
    expect = ""  # 预期结果
'''.format(**r)
    dic={}
    if "=" in data and method=="GET" and len(dic) == 0:
        req += "    params={}\n".format(str_to_dic(data))
        dic["params"]=None
    elif("=" in data and method=="POST" and len(dic) == 0):
        req += "    data={}\n".format(str_to_dic(data))
        kk = re.compile("'Content-Type': '(.*?)'")
        tt = kk.findall(req)
        print(tt)
        if(len(tt) == 1):
            b = "'Content-Type': '{}'".format(tt[0])
            req = req.replace(b,"'Content-Type': 'application/x-www-form-urlencoded'")
        dic["data"] = None

    try:
        s = json.loads(request_content)
        req += "    json_data='''{}'''\n".format(request_content)
        dic["json_data"] = None
    except:
        if "=" in request_content and len(dic) == 0:
            req += "    data={}\n".format(str_to_dic(request_content))
            dic["data"] = None
        elif len(dic) == 0:
            req += "    data='''{}'''\n".format(request_content)
            dic["data"] = None



    a = '''
    # --------------------分界线，下边的不要修改-----------------------------------------
    # method,pub_data和url为必传字段
    r = request_tool.request(method=method,url=uri,pub_data=pub_data,status_code=status_code,headers=headers,expect=expect,feature=feature,story=story,title=title'''
    req += a
    for d in dic:
        req += ",{}={}".format(d,d)
    req += ")"
    print(r)
    with open("demo.txt","w") as f:
        f.write(req)

    print(req)

if __name__ == '__main__':
    make_code()

