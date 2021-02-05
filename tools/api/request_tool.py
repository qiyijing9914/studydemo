'''
封装request
'''

import requests

from tools.report import log_tool
from tools.report.decorators_tool import logs, datas
import time


@datas
@logs
def request(*args,**kwargs):
    '''
    Get请求
    :param url:
    :param data:
    :param header:
    :return:
    '''
    try:
        response = requests.request(*args,**kwargs)
    except requests.RequestException as e:
        log_tool.error('%s%s' % ('Exception url: ', kwargs['url']))
        log_tool.error(e)
        return ()
    except Exception as e:
        log_tool.error('%s%s' % ('Exception url: ',kwargs['url']))
        return ()
    time_consuming = response.elapsed.microseconds / 1000
    log_tool.info('----请求用时: %s 秒数' % time_consuming)
    return response


@datas
@logs
def post_request(*args,**kwargs):
    '''
    Post请求
    :param url:
    :param data:
    :param header:
    :return:
    '''

    try:
        response = requests.post(*args,**kwargs)

    except requests.RequestException as e:
        log_tool.error('%s%s' % ('RequestException url: ',kwargs['url']))
        log_tool.error(e)
        return ()

    except Exception as e:
        log_tool.error('%s%s' % ('Exception url: ', kwargs['url']))
        log_tool.error(e)
        return ()

    # time_consuming为响应时间，单位为毫秒
    time_consuming = response.elapsed.microseconds / 1000
    log_tool.info('----请求用时: %s 秒数' % time_consuming)

    return response

@datas
@logs
def post_request_multipart(*args,**kwargs):
    '''
    提交Multipart/form-data 格式的Post请求
    :param url:
    :param data:
    :param header:
    :param file_parm:
    :param file:
    :param type:
    :return:
    '''

    response = requests.post(*args,**kwargs)
    # time_consuming为响应时间，单位为毫秒
    time_consuming = response.elapsed.microseconds / 1000
    log_tool.info('----请求用时: %s 秒数' % time_consuming)

    return response

@datas
@logs
def put_request(*args,**kwargs):
    '''
    Put请求
    :param url:
    :param data:
    :param header:
    :return:
    '''

    try:

        response = requests.put(*args,**kwargs)
    except requests.RequestException as e:
        log_tool.error('%s%s' % ('RequestException url: ', kwargs['url']))
        log_tool.error(e)
        return ()

    except Exception as e:
        print('%s%s' % ('Exception url: ', kwargs['url']))
        print(e)
        return ()

    time_consuming = response.elapsed.microseconds / 1000
    log_tool.info('----请求用时: %s 秒数' % time_consuming)

    return response

def down_big_file(srcUrl, localFile):
    print('%s\n --->>>\n  %s' % (srcUrl, localFile))
    startTime = time.time()
    with requests.get(srcUrl, stream=True) as r:
        contentLength = int(r.headers['content-length'])
        line = 'content-length: %dB/ %.2fKB/ %.2fMB'
        line = line % (contentLength, contentLength / 1024, contentLength / 1024 / 1024)
        print(line)
        print('正在下载中..............')
        downSize = 0
        with open(localFile, 'wb') as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
                downSize += len(chunk)
                line = '%d KB/s - %.2f MB， 共 %.2f MB'
                line = line % (
                downSize / 1024 / (time.time() - startTime), downSize / 1024 / 1024, contentLength / 1024 / 1024)
                print(line, end='\r')
                if downSize >= contentLength:
                    break
        timeCost = time.time() - startTime
        line = '共耗时: %.2f s, 平均速度: %.2f KB/s'
        line = line % (timeCost, downSize / 1024 / timeCost)
        print(line)
