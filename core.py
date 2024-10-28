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
    ls = sha256_encrypt("appSecret=Ew+ZSuppXZoA9YzBHgHmRvzt0Bw1CpwlQQtSl49QNhY=&channel=alipay&timestamp=" +
                        t+"&token="+token+"&version=1.60.3&"+url[25:])
    return ls


def sign(t, url, token):
    ls = sha256_encrypt("appSecret=nFU9pbG8YQoAe1kFh+E7eyrdlSLglwEJeA0wwHB1j5o=&channel=android_app&timestamp=" +
                        t+"&token="+token+"&version=1.60.3&"+url[25:])
    return ls


def httprequests(url, token, data, mean):
    t = str(int(time.time() * 1000))
    signs = sign(t, url, token)
    headers = {
        "Authorization": token,
        "Version": "1.60.3",
        "channel": "android_app",
        "phoneBrand": "Redmi",
        "timestamp": t,
        "sign": signs,
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Host": "userapi.qiekj.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": ua
    }
    if mean == "get":
        try:
            res = requests.get(url=url, headers=headers)
            if res.status_code == 200:
                res_json = json.loads(res.text)
                if res_json["msg"] == "未登录":
                    print(res_json["msg"])
                    exit()
                else:
                    return res_json
            else:
                print("请求出错❌\n", res.status_code, res.text)
                return None
        except requests.exceptions.Timeout:
            print("请求超时,即将重新请求")
            return "请求超时,即将重新请求"
        except Exception as e:
            print(e)
            print("请求出错❌退出")
            exit()
    elif mean == "post":
        try:
            res = requests.post(url=url, headers=headers, data=data)
            if res.status_code == 200:
                res_json = json.loads(res.text)
                # print(res_json)
                if res_json["msg"] == "未登录":
                    print(res_json["msg"])
                    exit()
                else:
                    return res_json
            else:
                print("出错❌\n", res.status_code, res.text)
                return None
        except requests.exceptions.Timeout:
            print("请求超时,即将重新请求")
            return "请求超时,即将重新请求"
        except Exception as e:
            print(e)
            print("出错❌退出")
            exit()

# 首页上滑商品获得定时积分


def sy(token):
    url = "https://userapi.qiekj.com/task/queryByType"
    data = {
        "taskCode": "8b475b42-df8b-4039-b4c1-f9a0174a611a",
        "token": token
    }
    res_json = httprequests(url, token, data, "post")
    if res_json["data"]["completedStatus"] == 1:
        print("首页浏览任务总次数限制-----跳过")
    else:
        url = "https://userapi.qiekj.com/task/completed"
        data1 = {"taskCode": "8b475b42-df8b-4039-b4c1-f9a0174a611a",
                 "subtaskCode": "4a86e8b5-e46c-4dac-9e73-c6e3cf39c7d6", "token": token}
        data2 = {"taskCode": "8b475b42-df8b-4039-b4c1-f9a0174a611a",
                 "subtaskCode": "73310f73-b076-40d5-a53f-c79c48f14d64", "token": token}
        data3 = {"taskCode": "8b475b42-df8b-4039-b4c1-f9a0174a611a",
                 "subtaskCode": "f3814d95-38f0-4778-8da3-6b8e3fc113d0", "token": token}
        time.sleep(1)
        res_json1 = httprequests(url=url, token=token, data=data1, mean="post")
        time.sleep(1)
        res_json2 = httprequests(url=url, token=token, data=data2, mean="post")
        time.sleep(1)
        res_json3 = httprequests(url=url, token=token, data=data3, mean="post")
        try:
            if res_json1["code"] == 0 and res_json1["data"] == True:
                print("首页浏览5s成功，获得5积分")
            if res_json2["code"] == 0 and res_json2["data"] == True:
                print("首页浏览10s成功，获得7积分")
            if res_json3["code"] == 0 and res_json3["data"] == True:
                print("首页浏览30s成功，获得10积分")
        except Exception as e:
            print(e)
            print(res_json1)
            print("首页浏览出错❌跳过")


def qd(token):
    url = "https://userapi.qiekj.com/signin/doUserSignIn"
    data = {"activityId": "600001", "token": token}
    res_json = httprequests(url=url, token=token, data=data, mean="post")
    try:
        if res_json["code"] == 0:
            print("签到成功，获得积分 "+str(res_json["data"]["totalIntegral"]))
        elif res_json["code"] == 33001:
            print("❗当天已经签到，请勿重复签到，重复签到容易账号异常")
        else:
            print("签到出错❌\n", res_json)
    except Exception as e:
        print("签到出错❌\n", res_json)


def zfbtask(token):
    url = "https://userapi.qiekj.com/task/completed"
    t = str(int(time.time() * 1000))
    signs = ''
    signs = signzfb(t, url, token)
    headers = {
        'Authorization': token,
        'Version': '1.60.3',
        'channel': 'alipay',
        'phoneBrand': 'Redmi',
        'timestamp': t,
        'sign': signs,
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Host': 'userapi.qiekj.com',
        'Accept-Encoding': 'gzip',
        'User-Agent': ua
    }
    data = {"taskCode": 9, "token": token}
    res_text = requests.post(url=url, headers=headers, data=data).text
    res_json = json.loads(res_text)
    return res_json


def tx(token, taskCode):
    url = "https://userapi.qiekj.com/task/completed"
    data = {"taskCode": taskCode, "token": token}
    res_json = httprequests(url=url, token=token, data=data, mean="post")
    return res_json


def appvideo(ua, token, i):
    url = "https://userapi.qiekj.com/task/completed"
    data = {"taskCode": 2, "token": token}
    res_json = httprequests(url=url, token=token, data=data, mean="post")
    if res_json['code'] == 0 and res_json['data'] == True:
        print('第'+str(i)+'次APP视频任务完成')
        return "t"
    else:
        # print('出错，跳过')
        # print(res_json)
        return "f"


def getusername(token):
    url = "https://userapi.qiekj.com/user/info"
    data = {"token": token}
    res_json = httprequests(url=url, data=data, token=token, mean="post")
    try:
        if res_json["code"] == 0:
            if res_json["data"]["userName"] == None:
                print("请去设置账号昵称")
            else:
                print("-----", res_json["data"]["userName"], "-----")
        else:
            print("❌")
            print(res_json)
    except:
        print("❌")
        print(res_json)


notfin = ["7328b1db-d001-4e6a-a9e6-6ae8d281ddbf", "e8f837b8-4317-4bf5-89ca-99f809bf9041",
          "65a4e35d-c8ae-4732-adb7-30f8788f2ea7", "73f9f146-4b9a-4d14-9d81-3a83f1204b74", "12e8c1e4-65d9-45f2-8cc1-16763e710036"]


def auto_sign(tk):
    getusername(token=tk)
    time.sleep(0.5)
    qd(token=tk)
    print("3s后开始执行任务")
    sy(token=tk)
    time.sleep(1)
    url = "https://userapi.qiekj.com/task/list"
    data = {"token": tk}
    res_json = httprequests(url=url, token=tk, data=data,mean="post")
    try:
        if res_json["code"] == 0:
            items = res_json["data"]["items"]
        else:
            print("❌获取任务列表失败，跳过任务")
            print(res_json)
    except Exception as e:
        print("获取任务列表失败，跳过任务")
        print(e)
    for item in items:
        if item['completedStatus'] == 0 and item["taskCode"] not in notfin:
            print("\n------任务分割线-----\n")
            print("开始执行任务  ——  ", item["title"])
            for num in range(item["dailyTaskLimit"]):
                res_json = tx(token=tk, taskCode=item["taskCode"])
                if res_json["code"] == 0:
                    time.sleep(1)
            print(item["title"], "  ——  任务完成")
            time.sleep(3)
    for num in range(5):
        flag = appvideo(ua=ua,token=tk,i=num+1)
        if flag == "f":
            break
        time.sleep(1)
    for num in range(5):
        res_json = zfbtask(token=tk)
        if res_json["code"] == 0 and res_json["data"] == True:
            print("第",str(num+1),"次支付宝视频")
        else:
            break
        time.sleep(1)
    time.sleep(1)
    url = "https://userapi.qiekj.com/user/balance"
    data = {"token": tk}
    res_json = httprequests(url=url, data=data, token=tk, mean="post")
    print("总积分：" + str(res_json['data']['integral']))
    print("所有任务均已完成------开始下一个账号\n\n\n")
    time.sleep(3)
    return "总积分：" + str(res_json["data"]["integral"])
