# coding=utf-8
import asyncio
import json
import time
from .core import auto_sign
import httpx

import httpx
from nonebot import on_command, require
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import (
    MessageEvent,
    Message,
)
from nonebot.matcher import Matcher
from nonebot.params import ArgPlainText, CommandArg

# from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State

require("nonebot_plugin_apscheduler")
require("nonebot_plugin_saa")
require("nonebot_plugin_localstore")

import nonebot_plugin_localstore as store
from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_saa import (
    MessageFactory,
    TargetQQGroup,
)

plugin_data_file = store.get_plugin_data_file("data.json")
if not plugin_data_file.exists():
    with open(plugin_data_file, "w") as file:
        json.dump([], file)

get_tk = on_command("开启自动签到", block=True, priority=1)


@get_tk.handle()
async def handle_function(
    matcher: Matcher, state: T_State, msg: Message = CommandArg()
):
    content = msg.extract_plain_text()
    if content == "" or content is None:
        await get_tk.finish("请输入胖乖生活绑定的手机号！", at_sender=True)

    url = "https://userapi.qiekj.com/common/sms/sendCode"
    headers = {
        "Version": "1.52.0",
        "channel": "android_app",
        "phoneBrand": "Redmi",
        "timestamp": str(int(time.time() * 1000)),
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Host": "userapi.qiekj.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.14.9",
    }

    data = {"phone": content, "template": "reg"}

    with httpx.Client(timeout=45) as client:
        response = client.post(url, headers=headers, data=data)
        if response.json()["code"] != 0:
            await get_tk.finish("获取胖乖生活验证码失败，请重试！", at_sender=True)
        state["phone"] = content


@get_tk.got("code_", prompt="请输入验证码")
async def got_name_(event: MessageEvent, state: T_State, code_: str = ArgPlainText()):
    if code_ == "停止":
        await get_tk.finish("已退出本次添加", at_sender=True)
    url = "https://userapi.qiekj.com/user/reg"
    headers = {
        "Version": "1.52.0",
        "channel": "android_app",
        "phoneBrand": "Redmi",
        "timestamp": str(int(time.time() * 1000)),
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Host": "userapi.qiekj.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.14.9",
    }

    data = {"channel": "android_app", "phone": state["phone"], "verify": code_}

    with httpx.Client(timeout=45) as client:
        response = client.post(url, headers=headers, data=data)
        try:
            token = response.json()["data"]["token"]
        except:
            await get_tk.reject(
                "获取胖乖生活验证码失败，请重新输入！输入“结束”中止本次添加",
                at_sender=True,
            )

    new_entry = {"id": event.user_id, "group": event.group_id, "token": token}

    with open(plugin_data_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    found = False
    for i, entry in enumerate(data):
        if entry.get("id") == new_entry.get("id"):
            data[i] = new_entry
            found = True
            break

    if not found:
        data.append(new_entry)

    with open(plugin_data_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    await get_tk.finish("成功开启胖乖生活自动签到！", at_sender=True)


@scheduler.scheduled_job("cron", hour=1, id="job_1")
async def run_1_hour():
    with open(plugin_data_file, "r") as file:
        t = json.load(file)
        loop = asyncio.get_event_loop()
        for i in t:
            res = await loop.run_in_executor(None, auto_sign, i["token"])
            target = TargetQQGroup(group_id=i["group"])
            await MessageFactory("用户" + str(i["id"]) + "，" + res).send_to(target)


run_now = on_command("立即签到", permission=SUPERUSER)


@run_now.handle()
async def _():
    await run_1_hour()
