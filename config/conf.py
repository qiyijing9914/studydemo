# API_URL="http://api.yansl.com:8084"
# API_URL="http://192.168.1.151:8084"
API_URL="http://172.16.25.52"


# GY_DB_QA = {
#     'host': '192.168.1.151',
#     'port': 3306,
#     'database': 'guoya_virtual_mall',
#     'user': 'stu123',
#     'password': 'stu123',
#     'charset': 'utf8'
# }
PAIDAN_DB_QA = {
    'host': '172.16.25.52',
    'port': 3306,
    'database': 'test2',
    'user': 'paidan_user',
    'password': 'aaA5y6C9vL',
    'charset': 'utf8'
}

GY_EMAIL_QA = {
    'on_off': 'on',  # 邮件是否发生，on发送，off不发送
    'mail_host': 'smtp.126.com',  # 设置服务器
    'mail_user': 'wuling1105@126.com',  # 用户名
    'mail_pass': '126shouquanma',  # 口令
    'sender': 'wuling1105@126.com',
    'mail_port': 25,
    'receivers': ['wuling@guoyasoft.com', 'wuling1105@126.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
}
