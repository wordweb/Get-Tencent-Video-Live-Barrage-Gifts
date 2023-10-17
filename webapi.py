import requests
import time
import qrcode
import uuid
import time
import json
import queue
import os
import uvicorn
import base64

from fastapi import FastAPI
from fastapi.responses import FileResponse

from threading import Thread, Lock, enumerate

#线程锁
app = FastAPI()
msglist = queue.Queue()
mutex = Lock()
terminate_flag=False
uid = uuid.uuid4().hex
uid22=str(uuid.uuid4())
uid33=str(uuid.uuid4())
session = requests.Session()
finderUsername=''
txvideo_nickname=''
txvideo_headImgUrl=''
wx_nickname=''
wx_username=''
wx_encryptedHeadImage=''
adminNickname=''
fansCount=0
uniqId=''
authKey=""
X_Wechat_Uin=""
liveObjectId=""
liveId=""
live_description=""
liveCookies=""

def filtertime():
    # 获取今天0点的时间戳
    today = time.time()
    filterEndTime = int(today) - (int(today) % 86400)

    # 减去 8664 天
    diff_days = 8664
    filterStartTime = filterEndTime - (diff_days * 86400)

    print("今天0点的时间戳：", filterEndTime)
    print("相减后的时间戳：", filterStartTime)    
    return filterEndTime,filterStartTime


def setcoockis(response):
    # 获取返回的cookie值
    cookies = response.cookies
    # 打印cookie值
    for cookie in cookies:
        print(cookie.name, cookie.value)

def generate_timestamp(length=10):
    current_time = time.time()
    if length == 10:
        timestamp = int(current_time)
    elif length == 13:
        timestamp = int(current_time * 1000)
    else:
        raise ValueError("Invalid timestamp length. Must be 10 or 13.")
    return  str(timestamp)

#初始化信息
def hepler_merlin_mmdata():
    url = "https://channels.weixin.qq.com/cgi-bin/mmfinderassistant-bin/helper/hepler_merlin_mmdata"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://channels.weixin.qq.com",
        "Referer": "https://channels.weixin.qq.com/platform/login-for-iframe?dark_mode=true&host_type=1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    time10=generate_timestamp(10)
    time13=generate_timestamp(13)
    data = {
        "id": 23865,
        "data": {
            "12": "",
            "13": "",
            "14": "",
            "15": "",
            "16": "",
            "17": time10,
            "18": time10,
            "19": 1,
            "20": "",
            "21": 2,
            "22": uid22,#"398e6d66-8c4d-45db-93f8-b13e240b0892",
            "23": "",
            "24": time13,
            "25": "",
            "26": 0,
            "27": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "28": "",
            "29": "",
            "30": "",
            "31": "LoginForIframe",
            "32": "",
            "33": uid33,#"556ff363-7c8b-4f2f-853e-79c35d51e4e7",
            "34": "",
            "35": "",
            "36": 1,
            "37": "{}",
            "38": "",
            "39": "{}",
            "40": "pageEnter",
            "41": "{}",
            "42": "{\"screenHeight\":1032;\"screenWidth\":1920;\"clientHeight\":0;\"clientWidth\":0}",
            "43": ""
        },
        "_log_finder_id": ""
    }

    response = session.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return None

#初始化信息2
def helper_mmdata():
    url = "https://channels.weixin.qq.com/cgi-bin/mmfinderassistant-bin/helper/helper_mmdata"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://channels.weixin.qq.com",
        "Referer": "https://channels.weixin.qq.com/platform/login-for-iframe?dark_mode=true&host_type=1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";=\"117\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    data = {
        "id": 21307,
        "data": {
            "13": "",
            "14": "",
            "15": "",
            "17": "null",
            "19": None,
            "20": None,
            "21": int(generate_timestamp(13)),
            "22": generate_timestamp(13)
        },
        "addFinderUinBy": 16
    }

    response = session.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return None





#获取登录二维码
def getrcode():
    url = "https://channels.weixin.qq.com/cgi-bin/mmfinderassistant-bin/auth/auth_login_code"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://channels.weixin.qq.com",
        "Referer": "https://channels.weixin.qq.com/platform/login-for-iframe?dark_mode=true&host_type=1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "X-WECHAT-UIN": "0000000000",
        "finger-print-device-id": uid,
        "sec-ch-ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }

    data = {
        "timestamp": str(int(time.time() * 1000)),  # 使用13位时间戳
        "_log_finder_uin": "",
        "_log_finder_id": "",
        "rawKeyBuff": None,
        "pluginSessionId": None,
        "scene": 7,
        "reqScene": 7
    }

    response = session.post(url, headers=headers, json=data)
    #setcoockis(response)
    redata=response.json()

    print(f'getrcode_errMesg:{redata["errMsg"]}')

    if 'token' in redata['data']:
        return redata['data']['token']

    return ''

def request_qrcode(retoken):
    url = f"https://channels.weixin.qq.com/cgi-bin/mmfinderassistant-bin/auth/auth_login_status?token={retoken}&timestamp={generate_timestamp(13)}&_log_finder_uin=&_log_finder_id=&scene=7&reqScene=7"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://channels.weixin.qq.com",
        "Referer": "https://channels.weixin.qq.com/platform/login-for-iframe?dark_mode=true&host_type=1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "X-WECHAT-UIN": "0000000000",
        "finger-print-device-id": uid,
        "sec-ch-ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }
    count = 0
    status= 0
    acctStatus = 0
    while count < 200:
        response = session.post(url, headers=headers)
        #setcoockis(response)
        rejson=response.json()
        if rejson['errCode'] == 0:
            # 处理返回的数据
            # ...
            status=rejson['data']['status']
            acctStatus=rejson['data']['acctStatus']
            if status==0 and acctStatus==0:
                print('请使用微信扫码登录！')
            elif status==5 and acctStatus==1:
                print('已扫码请在手机上点击确认登录！')
            elif status==1 and acctStatus==1:
                print('已成功登录！')
                break
            elif status==3 and acctStatus==0:
                print('已成功登录！')
                break
            else:
                print(rejson)
                print('超时或网络异常已退出')
                break

            count += 1
            time.sleep(1)
        else:
            print("请求失败")
            break

    if count >= 200:
        print("二维码已超时")
    if status==1 & acctStatus==1:
        return True
    return False


def auth_data():
    url = "https://channels.weixin.qq.com/cgi-bin/mmfinderassistant-bin/auth/auth_data"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://channels.weixin.qq.com",
        "Referer": "https://channels.weixin.qq.com/platform/login",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "X-WECHAT-UIN": "0000000000",
        "finger-print-device-id": uid,
        "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";=\"117\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    data = {
        "timestamp": generate_timestamp(13),
        "_log_finder_uin": "",
        "_log_finder_id": "",
        "rawKeyBuff": None,
        "pluginSessionId": None,
        "scene": 7,
        "reqScene": 7
    }

    response = session.post(url, headers=headers, json=data)
    #setcoockis(response)
    rejson=response.json()
    #print(response.json())
    if rejson['errCode'] == 0:
        global wx_encryptedHeadImage
        wx_encryptedHeadImage=rejson['data']['userAttr']['encryptedHeadImage']
        global wx_nickname
        wx_nickname=rejson['data']['userAttr']['nickname']
        global wx_username
        wx_username=rejson['data']['userAttr']['username']
        global txvideo_headImgUrl
        txvideo_headImgUrl=rejson['data']['finderUser']['headImgUrl']
        global txvideo_nickname
        txvideo_nickname=rejson['data']['finderUser']['nickname']
        global finderUsername
        finderUsername=rejson['data']['finderUser']['finderUsername']
        return True
    else:
        print("登录异常："+rejson['errMsg'])
        return False


def helper_upload_params():
    url = "https://channels.weixin.qq.com/cgi-bin/mmfinderassistant-bin/helper/helper_upload_params"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://channels.weixin.qq.com",
        "Referer": "https://channels.weixin.qq.com/platform/login",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "X-WECHAT-UIN": "0000000000",
        "finger-print-device-id": uid,
        "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    data = {
        "timestamp": generate_timestamp(13),
        "_log_finder_uin": "",
        "_log_finder_id": finderUsername,
        "rawKeyBuff": None,
        "pluginSessionId": None,
        "scene": 7,
        "reqScene": 7
    }

    response = session.post(url, headers=headers, json=data)
    rejson=response.json()
    if rejson['errCode'] == 0:
        global authKey
        authKey=rejson['data']['authKey']
        global X_Wechat_Uin
        X_Wechat_Uin=str(rejson['data']['uin'])
        return True
    else:
        return False



def check_live_status():
    url = "https://channels.weixin.qq.com/cgi-bin/mmfinderassistant-bin/live/check_live_status"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://channels.weixin.qq.com",
        "Referer": "https://channels.weixin.qq.com/platform/live/home",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "X-WECHAT-UIN": X_Wechat_Uin,
        "finger-print-device-id": uid,
        "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    data = {
        "timestamp": generate_timestamp(13),
        "_log_finder_uin": "",
        "_log_finder_id": finderUsername,
        "rawKeyBuff": None,
        "pluginSessionId": None,
        "scene": 7,
        "reqScene": 7
    }
    #print("check_live_status")
    try:
        response = session.post(url, headers=headers, json=data,timeout=30)

        rejson=response.json()
        if rejson['errCode'] == 0:
            global liveId
            liveId=rejson['data']['liveId']
            global live_description
            live_description=rejson['data']['description']
            global liveObjectId
            liveObjectId=rejson['data']['liveObjectId']
            #print("check_live_status end")
            if rejson['data']['status']==1:
                print(f'直播间【{live_description}】状态正常')
            else:
                print(f'直播间【{live_description}】状态={str(rejson["data"]["status"])}')
            return True
        else:
            return False
    except requests.exceptions.Timeout:
        print("check_live_status请求超时了")
        return True

#获取历史直播场次的记录。这里可以不用调用
def get_live_history():
    url = "https://channels.weixin.qq.com/cgi-bin/mmfinderassistant-bin/live/get_live_history"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://channels.weixin.qq.com",
        "Referer": "https://channels.weixin.qq.com/platform/live/home",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "X-WECHAT-UIN": X_Wechat_Uin,
        "finger-print-device-id": uid,
        "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";=\"117\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    request=filtertime()
    filterEndTime,filterStartTime=request
    #查询的开始和结束时间
    data = {
        "pageSize": 1,
        "currentPage": 1,
        "reqType": 2,
        "filterStartTime": filterStartTime,
        "filterEndTime": filterEndTime,
        "timestamp":generate_timestamp(13),
        "_log_finder_uin": "",
        "_log_finder_id": finderUsername,
        "rawKeyBuff": None,
        "pluginSessionId": None,
        "scene": 7,
        "reqScene": 7
    }

    response = session.post(url, headers=headers, json=data)

    rejson=response.json()
    if rejson['errCode'] == 0:
        return True
    else:
        return False

#
def get_live_info():
    url = "https://channels.weixin.qq.com/cgi-bin/mmfinderassistant-bin/live/get_live_info"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://channels.weixin.qq.com",
        "Referer": "https://channels.weixin.qq.com/platform/live/liveBuild",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "X-WECHAT-UIN": X_Wechat_Uin,
        "finger-print-device-id": uid,
        "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    data = {
        "liveObjectId": liveObjectId,
        "timestamp": generate_timestamp(13),
        "_log_finder_uin": "",
        "_log_finder_id": finderUsername,
        "rawKeyBuff": None,
        "pluginSessionId": None,
        "scene": 7,
        "reqScene": 7
    }
    #print('get_live_info')
    try:
        response = session.post(url, headers=headers, json=data,timeout=30)

        rejson=response.json()
        if rejson['errCode'] == 0:
            return True
        else:
            print(f"get_live_info异常：{rejson}")
            return False
    except requests.exceptions.Timeout:
        print("get_live_info请求超时了")
        return True

#获取msg消息刷新cookie
def join_live():
    url = "https://channels.weixin.qq.com/cgi-bin/mmfinderassistant-bin/live/join_live"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://channels.weixin.qq.com",
        "Referer": "https://channels.weixin.qq.com/platform/live/liveBuild",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "X-WECHAT-UIN": X_Wechat_Uin,
        "finger-print-device-id": uid,
        "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    data = {
        "objectId": liveObjectId,
        "finderUsername": finderUsername,
        "liveId": liveId,
        "timestamp": str(int(time.time() * 1000)), # 使用当前的时间戳
        "_log_finder_uin": "",
        "_log_finder_id": finderUsername,
        "rawKeyBuff": None,
        "pluginSessionId": None,
        "scene": 7,
        "reqScene": 7
    }

    response = session.post(url, headers=headers, json=data)

    rejson=response.json()
    if rejson['errCode'] == 0:
        global liveCookies
        liveCookies=rejson['data']['liveCookies']
        return True
    else:
        print(f"join_live异常：{rejson}")
        return False

#获取最新在线人员信息
def a_online_member():
    url = "https://channels.weixin.qq.com/cgi-bin/mmfinderassistant-bin/live/online_member"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://channels.weixin.qq.com",
        "Referer": "https://channels.weixin.qq.com/platform/live/liveBuild",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "X-WECHAT-UIN": X_Wechat_Uin,
        "finger-print-device-id": uid,
        "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    data = {
        "objectId": liveObjectId,
        "finderUsername": finderUsername,
        "clearRecentRewardHistory": True,
        "liveId": liveId,
        "timestamp": generate_timestamp(13),
        "_log_finder_uin": "",
        "_log_finder_id": finderUsername,
        "rawKeyBuff": None,
        "pluginSessionId": None,
        "scene": 7,
        "reqScene": 7
    }

    #print(f'online_member',data)
    #print('online_member')
    try:
        response = session.post(url, headers=headers, json=data,timeout=30)
        rejson=response.json()
        #print(rejson)
        if rejson['errCode'] == 0:
            json_str = json.dumps(rejson)
            # 将 JSON 字符串写入本地文件
            with open("online_member.json", "w") as file:
                file.write(json_str)
            return True
        else:
            print(f"online_member异常：{rejson}")
            return False
    except requests.exceptions.Timeout:
        print("online_member请求超时")
        return True




def msg():
    global liveCookies
    url = "https://channels.weixin.qq.com/cgi-bin/mmfinderassistant-bin/live/msg"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://channels.weixin.qq.com",
        "Referer": "https://channels.weixin.qq.com/platform/live/liveBuild",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "X-WECHAT-UIN": X_Wechat_Uin,
        "finger-print-device-id": uid,
        "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }

    data = {
        "objectId": liveObjectId,
        "finderUsername": finderUsername,
        "liveCookies": liveCookies,
        "liveId": liveId,
        "longpollingScene": 0,
        "timestamp": generate_timestamp(13),
        "_log_finder_uin": "",
        "_log_finder_id": finderUsername,
        "rawKeyBuff": None,
        "pluginSessionId": None,
        "scene": 7,
        "reqScene": 7
    }
    #print("msg")
    try:
        response = session.post(url, json=data, headers=headers,timeout=30)
        #print('msg1')
        rejson=response.json()
        #print('msg2')
        if rejson['errCode'] == 0:
            #对本次的消息进行解析

            liveCookies=rejson['data']['liveCookies']
            #print("liveCookies",liveCookies)
            downmsg(rejson['data'])
            return True
        else:
            return False
    except requests.exceptions.Timeout:
        print("msg请求超时了")
        return True

def reward_gains():
    url = "https://channels.weixin.qq.com/cgi-bin/mmfinderassistant-bin/live/reward_gains"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://channels.weixin.qq.com",
        "Referer": "https://channels.weixin.qq.com/platform/live/liveBuild",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "X-WECHAT-UIN": X_Wechat_Uin,
        "finger-print-device-id": uid,
        "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    data = {
        "objectId": liveObjectId,
        "finderUsername": finderUsername,
        "clearRecentRewardHistory": True,
        "liveId": liveId,
        "timestamp": generate_timestamp(13),
        "_log_finder_uin": "",
        "_log_finder_id": finderUsername,
        "rawKeyBuff": None,
        "pluginSessionId": None,
        "scene": 7,
        "reqScene": 7
    }
    #print("reward_gains")
    try:
        response = session.post(url, headers=headers, json=data,timeout=30)
        rejson=response.json()

        if rejson['errCode'] == 0:
            return True
        else:
            print('reward_gains_err:')
            print(rejson)
            return False
    except requests.exceptions.Timeout:
        print("reward_gains请求超时了")
        return True

def gift_enum_list():
    url = "https://channels.weixin.qq.com/cgi-bin/mmfinderassistant-bin/live/gift_enum_list"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://channels.weixin.qq.com",
        "Referer": "https://channels.weixin.qq.com/platform/live/liveBuild",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "X-WECHAT-UIN": X_Wechat_Uin,
        "finger-print-device-id": uid,
        "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    data = {
        "objectId": liveObjectId,
        "username": finderUsername,
        "liveId": liveId,
        "timestamp": generate_timestamp(13),
        "_log_finder_uin": "",
        "_log_finder_id": finderUsername,
        "rawKeyBuff": None,
        "pluginSessionId": None,
        "scene": 7,
        "reqScene": 7
    }
    
    response = session.post(url, headers=headers, json=data)
    rejson=response.json()
    print("gift_enum_list:")
    print(data)
    print(rejson)
    if rejson['errCode'] == 0:
        return True
    else:
        return False


def downmsg(rejson):
    #######解析数据########
    newmsg=[]
    for member in rejson['msgList']:
        type = member['type']
        if type==10005 :
            #print(member)
            nickname = member['nickname']
            username = member['username']
            content = member['content']
            signature=member['finderLiveContact']['contact']['signature']
            ext_info=member['finderLiveContact']['contact']['extInfo']
            badge_infos=member['finderLiveContact']['badgeInfos']
            newmsg.append({'nickname': nickname, 'msgType': type, 'username': username, 'content': content,'signature':signature,'ext_info':ext_info,'badge_infos':badge_infos})      
        if type==1 :
            #print(member)
            nickname = member['nickname']
            username = member['username']
            content = member['content']
            signature=member['finderLiveContact']['contact']['signature']
            ext_info=member['finderLiveContact']['contact']['extInfo']
            badge_infos=member['finderLiveContact']['badgeInfos']
            newmsg.append({'nickname': nickname, 'msgType': type, 'username': username, 'content': content,'signature':signature,'ext_info':ext_info,'badge_infos':badge_infos})   

    for member in rejson['appMsgList']:
        type=member['msgType']
        if type==20009:
            badge_infos=member['fromUserContact']['badgeInfos']
            nickname=member['fromUserContact']['contact']['nickname']
            username=member['fromUserContact']['contact']['username']
            signature=""
            ext_info=None
            base64_string = member['payload']
            decoded_string = base64.b64decode(base64_string).decode('utf-8')
            #print(decoded_string)
            gift_info=json.loads(decoded_string)
            newmsg.append({'nickname': nickname, 'msgType': type, 'username': username, 'gift_info': gift_info,'signature':signature,'ext_info':ext_info,'badge_infos':badge_infos})      





    ######################
    # 将数据写入文件
    # 检测当前目录下是否存在msglist目录，如果不存在则创建
    if not os.path.exists("msglist"):
        os.makedirs("msglist")

    # 生成文件路径
    file_path = os.path.join("msglist", f"{generate_timestamp(13)}.json")


  
    if len(newmsg)>0:
        # 将数据保存到文件中
        with open(file_path, "w") as file:
            json.dump(newmsg, file)





def getmsg():
    count = 0
    global terminate_flag
    while not terminate_flag:
        count += 1
        #print("当前时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        if get_live_info() and msg():
                time.sleep(0.1)
        else:
            break

        if count % 3 == 0:
            if check_live_status() and a_online_member() and reward_gains():
                time.sleep(0.1)
            else:
                break
        


@app.get("/getmsg")
def getmsgs():
    msglist_dir = "msglist"  # 指定目录路径

    # 检查目录是否存在
    if not os.path.exists(msglist_dir):
        return {"code": 0, "message": "目录不存在"}

    # 获取目录下的所有文件
    files = os.listdir(msglist_dir)

    # 检查是否有文件
    if len(files) == 0:
        return {"code": 0, "message": "目前没有消息"}

    # 取第一个文件
    first_file = files[0]

    # 构建文件路径
    file_path = os.path.join(msglist_dir, first_file)

    # 读取文件内容
    with open(file_path, "r") as file:
        file_content = file.read()

    # 删除已读取的文件
    os.remove(file_path)

    # 返回文件内容
    return {"code": 1, "message": "读取成功", "data": json.loads(file_content)}


@app.get("/clsmsg")
def clear_messages():
    msglist_dir = "msglist"  # 指定目录路径

    # 检查目录是否存在
    if not os.path.exists(msglist_dir):
        return {"code":0,"message": "目录不存在"}

    # 获取目录下的所有文件
    files = os.listdir(msglist_dir)

    # 删除目录下的所有文件
    for file in files:
        file_path = os.path.join(msglist_dir, file)
        os.remove(file_path)

    return {"code":1,"message": "所有文件已删除"}

@app.get("/get_online_member")
async def get_online_members():
    return FileResponse("online_member.json")

if __name__ == '__main__':
    t1 = Thread(target=getmsg)

    # 调用函数获取数据
    #data = hepler_merlin_mmdata()
    #print(data)
    # 调用函数发起请求
    #response = helper_mmdata()
    #print(response)

    retoken=getrcode()
    #print(retoken)
    rehttp=f'https://channels.weixin.qq.com/mobile/confirm_login.html?token={retoken}'

    qr = qrcode.QRCode()
    qr.border = 1
    qr.add_data(rehttp)
    qr.make()
    qr.print_ascii(out=None, tty=False, invert=False)

    print('请使用微信扫码登录！')

    time.sleep(1)

    # 获取二维码以及前期一系列准备工作。
    if request_qrcode(retoken) and auth_data() and helper_upload_params() and  check_live_status() and get_live_info() and join_live() and a_online_member():
        print("加载成功，开启消息获取线程。获取实时弹幕消息。")
        t1.start()


    
    #启动本地api服务
    print("如需关闭服务，请输入ctrl+C来终止api服务进程，再输入exit退出监听。")
    uvicorn.run("webapi:app", host="0.0.0.0", port=8000, reload=True)
    


    while True:
        user_input = input("等待输入指令：")
        print("用户输入的指令是：" + user_input)
        
        if user_input == "exit":
            terminate_flag=True
            t1.join()
            break