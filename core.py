import requests
import json
import time
import hashlib

REQUEST_ID_HEADER = "x-fc-request-id"
ua = "Mozilla/5.0 (Linux; U; Android 12; zh-Hans-CN; HBN-AL80 Build/HUAWEIHBN-AL80) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/100.0.4896.58 Quark/7.3.7.662 Mobile Safari/537.36"


def sha256_encrypt(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode("utf-8"))
    return sha256.hexdigest()


def signzfb(t, url, token):
    ls = sha256_encrypt(
        "appSecret=Ew+ZSuppXZoA9YzBHgHmRvzt0Bw1CpwlQQtSl49QNhY=&channel=alipay&timestamp="
        + t
        + "&token="
        + token
        + "&version=1.59.3&"
        + url[25:]
    )
    return ls


def sign(t, url, token):
    ls = sha256_encrypt(
        "appSecret=nFU9pbG8YQoAe1kFh+E7eyrdlSLglwEJeA0wwHB1j5o=&channel=android_app&timestamp="
        + t
        + "&token="
        + token
        + "&version=1.59.3&"
        + url[25:]
    )
    return ls


def qd(token):
    url = "https://userapi.qiekj.com/signin/signInAcList"
    t = str(int(time.time() * 1000))
    signs = ""
    signs = sign(t, url, token)
    headers = {
        "Authorization": token,
        "Version": "1.59.3",
        "channel": "android_app",
        "phoneBrand": "Redmi",
        "timestamp": t,
        "sign": signs,
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Host": "userapi.qiekj.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": ua,
    }
    data = {"token": token}
    res_text = requests.post(url=url, headers=headers, data=data).text
    try:
        res_json = json.loads(res_text)
        if res_json["code"] == 0:
            url = "https://userapi.qiekj.com/signin/doUserSignIn"
            t = str(int(time.time() * 1000))
            signs = ""
            signs = sign(t, url, token)
            headers = {
                "Authorization": token,
                "Version": "1.59.3",
                "channel": "android_app",
                "phoneBrand": "Redmi",
                "timestamp": t,
                "sign": signs,
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "Host": "userapi.qiekj.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": ua,
            }
            data = {"activityId": "600001", "token": token}
            res_text = requests.post(url=url, headers=headers, data=data).text
            res_json = json.loads(res_text)
            print("签到成功，获得积分 " + str(res_json["data"]["totalIntegral"]))
    except:
        print("出错")
        print(res_text)


def taskrequests(ua, url, token, data):
    t = str(int(time.time() * 1000))
    signs = ""
    signs = sign(t, url, token)
    headers = {
        "Authorization": token,
        "Version": "1.59.3",
        "channel": "android_app",
        "phoneBrand": "Redmi",
        "timestamp": t,
        "sign": signs,
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Host": "userapi.qiekj.com",
        "Accept-Encoding": "gzip",
        "User-Agent": ua,
    }
    res_text = requests.post(url=url, headers=headers, data=data).text
    res_json = json.loads(res_text)
    return res_json


def tx(ua, token, tc):
    url = "https://userapi.qiekj.com/task/completed"
    data = {"taskCode": tc, "token": token}
    res_json = taskrequests(ua, url, token, data)
    return res_json


def ladderTask(ua, token):
    url = "https://userapi.qiekj.com/ladderTask/ladderTaskForDay?token=" + token
    t = str(int(time.time() * 1000))
    signs = ""
    signs = sign(t, "https://userapi.qiekj.com/ladderTask/ladderTaskForDay", token)
    headers = {
        "Authorization": token,
        "Version": "1.57.4",
        "channel": "android_app",
        "phoneBrand": "Redmi",
        "timestamp": t,
        "sign": signs,
        "Host": "userapi.qiekj.com",
        "Accept-Encoding": "gzip",
        "User-Agent": ua,
    }
    res_json = json.loads(requests.get(url=url, headers=headers).text)
    if res_json["code"] == 0:
        ladderRewardList = res_json["data"]["ladderRewardList"]
        for item in ladderRewardList:
            if item["isApplyReward"] == 1:
                data = {"rewardCode": item["rewardCode"], "token": token}
                success = taskrequests(
                    ua,
                    "https://userapi.qiekj.com/ladderTask/applyLadderReward",
                    token,
                    data,
                )
                print(success)
                time.sleep(2)
        print("阶梯任务领奖完成")
    else:
        print("阶梯任务领取失败")
        print(res_json)


def appvideo(ua, token, i):
    url = "https://userapi.qiekj.com/task/completed"
    data = {"taskCode": 2, "token": token}
    res_json = taskrequests(ua, url, token, data)
    if res_json["code"] == 0:
        print("第" + str(i) + "次APP视频任务完成")
    else:
        print("出错，跳过")
        print(res_json)


def chaAD(ua, token, i):
    url = "https://userapi.qiekj.com/task/completed"
    data = {"taskCode": "18893134-715b-4307-af1c-b5737c70f58d", "token": token}
    res_json = taskrequests(ua, url, token, data)
    if res_json["code"] == 0:
        print("第" + str(i) + "次APP视频任务完成")
    else:
        print("出错，跳过")
        print(res_json)


def sytask(ua, token):
    url = "https://userapi.qiekj.com/task/completed"
    data1 = {
        "taskCode": "8b475b42-df8b-4039-b4c1-f9a0174a611a",
        "subtaskCode": "4a86e8b5-e46c-4dac-9e73-c6e3cf39c7d6",
        "token": token,
    }
    data2 = {
        "taskCode": "8b475b42-df8b-4039-b4c1-f9a0174a611a",
        "subtaskCode": "73310f73-b076-40d5-a53f-c79c48f14d64",
        "token": token,
    }
    data3 = {
        "taskCode": "8b475b42-df8b-4039-b4c1-f9a0174a611a",
        "subtaskCode": "f3814d95-38f0-4778-8da3-6b8e3fc113d0",
        "token": token,
    }
    res_json1 = taskrequests(ua, url, token, data1)
    res_json2 = taskrequests(ua, url, token, data2)
    res_json3 = taskrequests(ua, url, token, data3)
    try:
        if res_json1["code"] == 0 and res_json1["data"] == True:
            print("首页浏览5s成功，获得5积分")
        if res_json2["code"] == 0 and res_json2["data"] == True:
            print("首页浏览10s成功，获得7积分")
        if res_json3["code"] == 0 and res_json3["data"] == True:
            print("首页浏览30s成功，获得10积分")
    except:
        print("首页浏览出错❌")


def taskl(ua, url, token, data):
    t = str(int(time.time() * 1000))
    signs = ""
    signs = signzfb(t, url, token)
    headers = {
        "Authorization": token,
        "Version": "1.59.3",
        "channel": "alipay",
        "phoneBrand": "Redmi",
        "timestamp": t,
        "sign": signs,
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Host": "userapi.qiekj.com",
        "Accept-Encoding": "gzip",
        "User-Agent": ua,
    }
    res_text = requests.post(url=url, headers=headers, data=data).text
    res_json = json.loads(res_text)
    return res_json


def gettoadyamount(ua, token):
    url = "https://userapi.qiekj.com/integralRecord/pageList"
    t = str(int(time.time() * 1000))
    signs = ""
    signs = sign(t, url, token)
    headers = {
        #'Authorization': token,
        "Version": "1.59.3",
        "channel": "android_app",
        "phoneBrand": "Redmi",
        "timestamp": t,
        "sign": signs,
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary3vwDBVnGIm81La5R",
        "Host": "userapi.qiekj.com",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": ua,
        "Referer": "http://h5user.qiekj.com/",
    }
    # 定义表单数据
    files = {
        ("page", ""): (None, "1"),
        ("pageSize", ""): (None, "50"),
        ("type", ""): (None, "100"),
        ("role", ""): (None, "1"),
        ("token", ""): (None, "84d2815ff6f0e87b2c3ca4105e42f"),
    }
    res_json = requests.post(url=url, headers=headers, files=files).text
    print(res_json)


notfin = [
    "7328b1db-d001-4e6a-a9e6-6ae8d281ddbf",
    "e8f837b8-4317-4bf5-89ca-99f809bf9041",
    "65a4e35d-c8ae-4732-adb7-30f8788f2ea7",
    "73f9f146-4b9a-4d14-9d81-3a83f1204b74",
]


def auto_sign(tk):
    sytask(ua=ua, token=tk)
    try:
        print("开始签到任务")
        qd(tk)
    except:
        print("出错：账号" + tk)
    finally:
        time.sleep(3)
    url = "https://userapi.qiekj.com/task/list"
    data = {"token": tk}
    res_json = taskrequests(ua, url, tk, data)
    items = res_json["data"]["items"]
    try:
        if res_json["code"] == 0:
            items = res_json["data"]["items"]
            for item in items:
                if item["completedStatus"] == 0 and item["taskCode"] not in notfin:
                    print("\n------任务分割线-----\n")
                    print("开始执行任务  ——  ", item["title"])
                    for num in range(item["dailyTaskLimit"]):
                        res_json = tx(ua, tk, item["taskCode"])
                        if res_json["code"] == 0:
                            time.sleep(1)
                    print(item["title"], "  ——  任务完成")
                time.sleep(3)
            for num in range(5):
                appvideo(ua=ua, token=tk, i=num + 1)
                time.sleep(1)
            for num in range(5):
                tx(ua, tk, "9")
                print("第", str(num + 1), "次支付宝视频")
                time.sleep(1)
            ladderTask(ua, tk)

    except:
        print("出错")
        print(res_json)
    finally:
        url = "https://userapi.qiekj.com/user/balance"
        data = {"token": tk}
        res_json = taskrequests(ua, url, tk, data)
        return "总积分：" + str(res_json["data"]["integral"])
