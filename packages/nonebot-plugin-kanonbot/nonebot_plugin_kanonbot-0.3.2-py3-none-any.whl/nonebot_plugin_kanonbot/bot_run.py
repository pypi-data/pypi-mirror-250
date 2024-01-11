# coding=utf-8
import re

from .config import _config_list
from .tools import kn_config, lockst, locked, command_cd, get_command
from .plugins import (
    plugin_zhanbu, plugin_config, plugin_emoji_xibao, plugin_emoji_yizhi, plugin_game_cck, plugin_game_blowplane,
    plugin_checkin, plugin_emoji_keai, plugin_emoji_jiehun, plugin_emoji_momo,
    plugin_emoji_emoji, plugin_jellyfish_box
)
import time
import nonebot
from nonebot import logger
import os
import sqlite3

try:
    config = nonebot.get_driver().config
    # 配置1
    try:
        adminqq = list(config.superusers)
    except Exception as e:
        adminqq = []
    # 配置2：
    try:
        basepath = config.kanonbot_basepath
        if "\\" in basepath:
            basepath = basepath.replace("\\", "/")
        if basepath.startswith("./"):
            basepath = os.path.abspath('.') + basepath.removeprefix(".")
            if not basepath.endswith("/"):
                basepath += "/"
        else:
            if not basepath.endswith("/"):
                basepath += "/"
    except Exception as e:
        basepath = os.path.abspath('.') + "/KanonBot/"
except Exception as e:
    adminqq = []
    basepath = os.path.abspath('.') + "/KanonBot/"
if not os.path.exists(basepath):
    os.makedirs(basepath)

if "\\" in basepath:
    basepath = basepath.replace("\\", "/")


async def botrun(msg_info):
    logger.info("KanonBot-0.3.2")
    # ## 初始化 ##
    lockdb = f"{basepath}db/"
    if not os.path.exists(lockdb):
        os.makedirs(lockdb)
    lockdb += "lock.db"
    await lockst(lockdb)
    msg: str = msg_info["msg"]
    commands: list = msg_info["commands"]
    command: str = commands[0]
    if len(commands) >= 2:
        command2 = commands[1]
        # 去除前后空格
        while len(command2) > 0 and command2.startswith(" "):
            command2 = command2.removeprefix(" ")
        while len(command2) > 0 and command2.endswith(" "):
            command2 = command2.removesuffix(" ")
    else:
        command2 = None
    at_datas: list = msg_info["at_datas"]
    user_permission:int = int(msg_info["user"]["permission"])
    user_id: str = msg_info["user"]["user_id"]
    if "face_image" in list(msg_info["user"]):
        user_avatar = msg_info["user"]["face_image"]
    else:
        user_avatar = None
    if msg_info["user"]["nick_name"] is not None:
        user_name: str = msg_info["user"]["nick_name"]
    else:
        user_name: str = msg_info["user"]["username"]
    commandname: str = msg_info["commandname"]
    guild_id: str = msg_info["guild_id"]
    channel_id: str = msg_info["channel_id"]
    imgmsgs = msg_info["imgmsgs"]
    botid: str = msg_info["bot_id"]
    friend_list: list = msg_info["friend_list"]
    group_member_datas = msg_info["channel_member_datas"]
    event_name: str = msg_info["event_name"]

    username = None
    qq2name = None

    # ## 变量初始化 ##
    date: str = time.strftime("%Y-%m-%d", time.localtime())
    date_year: str = time.strftime("%Y", time.localtime())
    date_month: str = time.strftime("%m", time.localtime())
    date_day: str = time.strftime("%d", time.localtime())
    time_h: str = time.strftime("%H", time.localtime())
    time_m: str = time.strftime("%M", time.localtime())
    time_s: str = time.strftime("%S", time.localtime())
    time_now: int = int(time.time())

    cachepath = f"{basepath}cache/{date_year}/{date_month}/{date_day}/"
    if not os.path.exists(cachepath):
        os.makedirs(cachepath)

    def del_files2(dir_path):
        """
        删除文件夹下所有文件和路径，保留要删的父文件夹
        """
        for root, dirs, files in os.walk(dir_path, topdown=False):
            # 第一步：删除文件
            for name in files:
                os.remove(os.path.join(root, name))  # 删除文件
            # 第二步：删除空文件夹
            for name in dirs:
                os.rmdir(os.path.join(root, name))  # 删除一个空目录

    # 清除缓存
    if os.path.exists(f"{basepath}/cache/{int(date_year) - 1}"):
        filenames = os.listdir(f"{basepath}/cache/{int(date_year) - 1}")
        if filenames:
            del_files2(f"{basepath}/cache/{int(date_year) - 1}")
    elif os.path.exists(f"{basepath}/cache/{date_year}/{int(date_month) - 1}"):
        filenames = os.listdir(f"{basepath}/cache/{date_year}/{int(date_month) - 1}")
        if filenames:
            del_files2(f"{basepath}/cache/{date_year}/{int(date_month) - 1}")
    elif os.path.exists(f"{basepath}/cache/{date_year}/{date_month}/{int(date_day) - 1}"):
        filenames = os.listdir(f"{basepath}/cache/{date_year}/{date_month}/{int(date_day) - 1}")
        if filenames:
            del_files2(f"{basepath}/cache/{date_year}/{date_month}/{int(date_day) - 1}")

    dbpath = basepath + "db/"
    if not os.path.exists(dbpath):
        os.makedirs(dbpath)

    # ## 初始化回复内容 ##
    returnpath = None
    returnpath2 = None
    returnpath3 = None
    message = None
    reply = False
    at = False
    code = 0
    cut = 'off'
    run = True

    # 添加函数
    # 查询功能开关
    def getconfig(commandname: str) -> bool:
        """
        查询指令是否开启
        :param commandname: 查询的命令名
        :return: True or False
        """
        conn = sqlite3.connect(f"{basepath}db/config.db")
        cursor = conn.cursor()
        state = False
        try:
            if not os.path.exists(f"{basepath}db/config.db"):
                # 数据库文件 如果文件不存在，会自动在当前目录中创建
                cursor.execute(f"create table {guild_id}(command VARCHAR(10) primary key, state BOOLEAN(20))")
            cursor.execute("SELECT * FROM sqlite_master WHERE type='table'")
            datas = cursor.fetchall()
            tables = []
            for data in datas:
                if data[1] != "sqlite_sequence":
                    tables.append(data[1])
            if guild_id not in tables:
                cursor.execute(f"create table {guild_id}(command VARCHAR(10) primary key, state BOOLEAN(20))")
            cursor.execute(f'SELECT * FROM {guild_id} WHERE command = "{channel_id}-{commandname}"')
            data = cursor.fetchone()
            if data is not None:
                state = data[1]
            else:
                cursor.execute("SELECT * FROM sqlite_master WHERE type='table'")
                datas = cursor.fetchall()
                # 数据库列表转为序列
                tables = []
                for data in datas:
                    if data[1] != "sqlite_sequence":
                        tables.append(data[1])
                if "list" not in tables:
                    cursor.execute("create table list(command VARCHAR(10) primary key, state BOOLEAN(20), "
                                   "message VARCHAR(20), 'group' VARCHAR(20), name VARCHAR(20))")
                cursor.execute(f'SELECT * FROM list WHERE command="{channel_id}-{commandname}"')
                data = cursor.fetchone()
                if data is not None:
                    state = data[1]
                    cursor.execute(
                        f'replace into {guild_id} ("command","state") values("{channel_id}-{commandname}",{state})')
                    conn.commit()
                else:
                    config_list = _config_list()
                    if commandname in list(config_list):
                        state = config_list[commandname]["state"]
                    else:
                        state = False
        finally:
            pass
        cursor.close()
        conn.close()
        return state

    # ## 心跳服务相关 ##
    # 判断心跳服务是否开启。
    if kn_config("botswift-state"):
        # 读取忽略该功能的群聊
        ignore_list = kn_config("botswift-ignore_list")
        if guild_id.startswith("channel-"):
            if guild_id[8:] in kn_config("botswift-ignore_list"):
                run = True
        elif guild_id.startswith("group-"):
            if guild_id[6:] in kn_config("botswift-ignore_list"):
                run = True

    # 处理消息
    if commandname.startswith("config"):
        if user_permission == 7 or user_id in adminqq or commandname == "config查询":
            pass
        run = True
        if run:
            logger.info(f"run-{commandname}")
            if command2 is not None:
                config_name = get_command(command2)[0]
            else:
                config_name = None
            message, returnpath = plugin_config(commandname, config_name, channel_id)
            if message is not None:
                code = 1
            else:
                code = 2
        else:
            logger.info(f"run-{commandname}, 用户权限不足")
            code = 1
            message = "权限不足"

    elif commandname.startswith("群聊功能-"):
        commandname = commandname.removeprefix("群聊功能-")
        if "zhanbu" == commandname and getconfig(commandname):
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    at = True
                    logger.info(f"run-{commandname}")
                    message, returnpath = await plugin_zhanbu(user_id, cachepath)
                    if returnpath is not None:
                        code = 3
                    else:
                        code = 1
            else:
                at = True
                logger.info(f"run-{commandname}")
                message, returnpath = await plugin_zhanbu(user_id, cachepath)
                if returnpath is not None:
                    code = 3
                else:
                    code = 1
        elif "签到" == commandname and getconfig(commandname):
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    state, message = await plugin_checkin(user_id=user_id, group_id=guild_id, date=date)
                    code = 1
            else:
                logger.info(f"run-{commandname}")
                state, message = await plugin_checkin(user_id=user_id, group_id=guild_id, date=date)
                code = 1
        elif "水母箱" == commandname and getconfig(commandname):
            if command2 is not None and command == "水母箱":
                command = command2
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    code, message, returnpath = await plugin_jellyfish_box(
                        user_id=user_id,
                        user_name=user_name,
                        channel_id=channel_id,
                        msg=command,
                        time_now=time_now
                    )
            else:
                logger.info(f"run-{commandname}")
                code, message, returnpath = await plugin_jellyfish_box(
                    user_id=user_id,
                    user_name=user_name,
                    channel_id=channel_id,
                    msg=command,
                    time_now=time_now
                )

    elif commandname.startswith("表情功能-"):
        commandname = commandname.removeprefix("表情功能-")
        if "emoji" == commandname and getconfig(commandname):
            if command == "合成":
                command = command2
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    message, returnpath = await plugin_emoji_emoji(command)
                    if message is not None:
                        code = 1
                    else:
                        code = 2
            else:
                logger.info(f"run-{commandname}")
                message, returnpath = await plugin_emoji_emoji(command)
                if message is not None:
                    code = 1
                else:
                    code = 2
        elif "喜报" == commandname and getconfig(commandname):
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    returnpath = await plugin_emoji_xibao(command, command2, imgmsgs)
                    code = 2
            else:
                logger.info(f"run-{commandname}")
                returnpath = await plugin_emoji_xibao(command, command2, imgmsgs)
                code = 2
        elif "一直" == commandname and getconfig(commandname):
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    if imgmsgs:
                        returnpath = await plugin_emoji_yizhi(imgmsgs[0])
                    else:
                        returnpath = await plugin_emoji_yizhi(user_avatar)
                    code = 2
            else:
                logger.info(f"run-{commandname}")
                if imgmsgs:
                    returnpath = await plugin_emoji_yizhi(imgmsgs[0])
                else:
                    returnpath = await plugin_emoji_yizhi(user_avatar)
                code = 2
        elif "可爱" == commandname and getconfig(commandname):
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    if command2 is not None:
                        user_name = command2
                    if imgmsgs:
                        returnpath = await plugin_emoji_keai(imgmsgs[0], user_name)
                    else:
                        returnpath = await plugin_emoji_keai(user_avatar, user_name)
                    code = 2
            else:
                logger.info(f"run-{commandname}")
                if imgmsgs:
                    returnpath = await plugin_emoji_keai(imgmsgs[0], user_name)
                else:
                    returnpath = await plugin_emoji_keai(user_avatar, user_name)
                code = 2
        elif "结婚" == commandname and getconfig(commandname):
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    if command2 is not None:
                        if " " in command2:
                            command2 = command2.split(" ", 1)
                            name1 = command2[0]
                            name2 = command2[1]
                        else:
                            name1 = user_name
                            name2 = command2
                    else:
                        name1 = user_name
                        name2 = " "
                    if imgmsgs:
                        returnpath = await plugin_emoji_jiehun(imgmsgs[0], name1, name2)
                    else:
                        returnpath = await plugin_emoji_jiehun(user_avatar, name1, name2)
                    code = 2
            else:
                logger.info(f"run-{commandname}")
                if command2 is not None:
                    if " " in command2:
                        command2 = command2.split(" ", 1)
                        name1 = command2[0]
                        name2 = command2[1]
                    else:
                        name1 = user_name
                        name2 = command2
                else:
                    name1 = user_name
                    name2 = " "
                if imgmsgs:
                    returnpath = await plugin_emoji_jiehun(imgmsgs[0], name1, name2)
                else:
                    returnpath = await plugin_emoji_jiehun(user_avatar, name1, name2)
                code = 2
        elif "摸摸" == commandname and getconfig(commandname):
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    if imgmsgs:
                        returnpath = await plugin_emoji_momo(imgmsgs[0])
                    else:
                        returnpath = await plugin_emoji_momo(user_avatar)
                    code = 2
            else:
                logger.info(f"run-{commandname}")
                if imgmsgs:
                    returnpath = await plugin_emoji_momo(imgmsgs[0])
                else:
                    returnpath = await plugin_emoji_momo(user_avatar)
                code = 2
        elif "亲亲" == commandname and getconfig(commandname):
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    if imgmsgs:
                        returnpath = await plugin_emoji_qinqin(imgmsgs[0])
                    else:
                        returnpath = await plugin_emoji_qinqin(user_avatar)
                    code = 2
            else:
                logger.info(f"run-{commandname}")
                if imgmsgs:
                    returnpath = await plugin_emoji_qinqin(imgmsgs[0])
                else:
                    returnpath = await plugin_emoji_qinqin(user_avatar)
                code = 2
        elif "贴贴" == commandname and getconfig(commandname):
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    if imgmsgs:
                        returnpath = await plugin_emoji_tietie(imgmsgs[0])
                    else:
                        returnpath = await plugin_emoji_tietie(user_avatar)
                    code = 2
            else:
                logger.info(f"run-{commandname}")
                if imgmsgs:
                    returnpath = await plugin_emoji_tietie(imgmsgs[0])
                else:
                    returnpath = await plugin_emoji_tietie(user_avatar)
                code = 2
        elif "逮捕" == commandname and getconfig(commandname):
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    if imgmsgs:
                        returnpath = await plugin_emoji_daibu(imgmsgs[0])
                    else:
                        returnpath = await plugin_emoji_daibu(user_avatar)
                    code = 2
            else:
                logger.info(f"run-{commandname}")
                if imgmsgs:
                    returnpath = await plugin_emoji_daibu(imgmsgs[0])
                else:
                    returnpath = await plugin_emoji_daibu(user_avatar)
                code = 2
        elif "踢" == commandname and getconfig(commandname):
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    if imgmsgs:
                        returnpath = await plugin_emoji_ti(imgmsgs[0])
                    else:
                        returnpath = await plugin_emoji_ti(user_avatar)
                    code = 2
            else:
                logger.info(f"run-{commandname}")
                if imgmsgs:
                    returnpath = await plugin_emoji_ti(imgmsgs[0])
                else:
                    returnpath = await plugin_emoji_ti(user_avatar)
                code = 2
        elif "爬" == commandname and getconfig(commandname):
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    if imgmsgs:
                        returnpath = await plugin_emoji_pa(imgmsgs[0])
                    else:
                        returnpath = await plugin_emoji_pa(user_avatar)
                    code = 2
            else:
                logger.info(f"run-{commandname}")
                if imgmsgs:
                    returnpath = await plugin_emoji_pa(imgmsgs[0])
                else:
                    returnpath = await plugin_emoji_pa(user_avatar)
                code = 2
        elif "咬咬" == commandname and getconfig(commandname):
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    if imgmsgs:
                        returnpath = await plugin_emoji_yaoyao(imgmsgs[0])
                    else:
                        returnpath = await plugin_emoji_yaoyao(user_avatar)
                    code = 2
            else:
                logger.info(f"run-{commandname}")
                if imgmsgs:
                    returnpath = await plugin_emoji_yaoyao(imgmsgs[0])
                else:
                    returnpath = await plugin_emoji_yaoyao(user_avatar)
                code = 2
        elif "寄" == commandname and getconfig(commandname):
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    if imgmsgs:
                        returnpath = await plugin_emoji_ji()
                    else:
                        returnpath = await plugin_emoji_ji()
                    code = 2
            else:
                logger.info(f"run-{commandname}")
                if imgmsgs:
                    returnpath = await plugin_emoji_ji()
                else:
                    returnpath = await plugin_emoji_ji()
                code = 2
        elif "拳拳" == commandname and getconfig(commandname):
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    if imgmsgs:
                        returnpath = await plugin_emoji_quanquan(imgmsgs[0])
                    else:
                        returnpath = await plugin_emoji_quanquan(user_avatar)
                    code = 2
            else:
                logger.info(f"run-{commandname}")
                if imgmsgs:
                    returnpath = await plugin_emoji_quanquan(imgmsgs[0])
                else:
                    returnpath = await plugin_emoji_quanquan(user_avatar)
                code = 2
        elif "我老婆" == commandname and getconfig(commandname):
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    if imgmsgs:
                        returnpath = await plugin_emoji_wolaopo(imgmsgs[0])
                    else:
                        returnpath = await plugin_emoji_wolaopo(user_avatar)
                    code = 2
            else:
                logger.info(f"run-{commandname}")
                if imgmsgs:
                    returnpath = await plugin_emoji_wolaopo(imgmsgs[0])
                else:
                    returnpath = await plugin_emoji_wolaopo(user_avatar)
                code = 2
        elif "指" == commandname and getconfig(commandname):
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    if imgmsgs:
                        returnpath = await plugin_emoji_zhi(imgmsgs[0])
                    else:
                        returnpath = await plugin_emoji_zhi(user_avatar)
                    code = 2
            else:
                logger.info(f"run-{commandname}")
                if imgmsgs:
                    returnpath = await plugin_emoji_zhi(imgmsgs[0])
                else:
                    returnpath = await plugin_emoji_zhi(user_avatar)
                code = 2
        elif "结婚证" == commandname and getconfig(commandname):
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    if imgmsgs:
                        returnpath = await plugin_emoji_jiehunzheng(imgmsgs[0])
                    else:
                        returnpath = await plugin_emoji_jiehunzheng(user_avatar)
                    code = 2
            else:
                logger.info(f"run-{commandname}")
                if imgmsgs:
                    returnpath = await plugin_emoji_jiehunzheng(imgmsgs[0])
                else:
                    returnpath = await plugin_emoji_jiehunzheng(user_avatar)
                code = 2
        elif "急" == commandname and getconfig(commandname):
            if getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id,
                    groupcode=channel_id,
                    timeshort=time_now,
                    coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    if imgmsgs:
                        returnpath = await plugin_emoji_ji2(imgmsgs[0])
                    else:
                        returnpath = await plugin_emoji_ji2(user_avatar)
                    code = 2
            else:
                logger.info(f"run-{commandname}")
                if imgmsgs:
                    returnpath = await plugin_emoji_ji2(imgmsgs[0])
                else:
                    returnpath = await plugin_emoji_ji2(user_avatar)
                code = 2

    elif commandname.startswith("小游戏"):
        commandname = commandname.removeprefix("小游戏-")
        if "猜猜看" == commandname and getconfig(commandname):
            # 转换命令名
            if command2 is not None:
                command = command2
            if command == "cck":
                command = "猜猜看"
            elif command == "bzd":
                command = "不知道"
            elif command == "结束":
                command = "不知道"

            # 判断指令冷却
            if command == "猜猜看" and getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id, groupcode=channel_id, timeshort=time_now, coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    code, message, returnpath = await plugin_game_cck(command=command, channel_id=channel_id)
            else:
                logger.info(f"run-{commandname}")
                code, message, returnpath = await plugin_game_cck(command=command, channel_id=channel_id)
        elif "炸飞机" == commandname and getconfig(commandname):
            # 转换命令名
            if command.startswith("炸") and not command.startswith("炸飞机"):
                command = command.removeprefix("炸")
            if command2 is not None:
                command = command2
            if command == "zfj":
                command = "炸飞机"

            # 判断指令冷却
            if command == "炸飞机" and getconfig("commandcd"):
                cooling = command_cd(
                    user_id=user_id, groupcode=channel_id, timeshort=time_now, coolingdb=f"{dbpath}cooling.db")
                if cooling != "off" and user_permission != "7" and user_id not in adminqq:
                    code = 1
                    message = f"指令冷却中（{cooling}s)"
                    logger.info("指令冷却中")
                else:
                    logger.info(f"run-{commandname}")
                    code, message, returnpath = await plugin_game_blowplane(command=command, channel_id=channel_id)
            else:
                logger.info(f"run-{commandname}")
                code, message, returnpath = await plugin_game_blowplane( command=command, channel_id=channel_id)

    elif "###" == commandname:
        pass

    # 这两位置是放心跳服务相关代码，待后续完善
    # 本bot存入mainbot数据库
    # 保活

    # log记录
    # 目前还不需要这个功能吧，先放着先

    # 返回消息处理
    locked(lockdb)
    return {"code": code,
            "message": message,
            "returnpath": returnpath,
            "returnpath2": returnpath2,
            "returnpath3": returnpath3
            }
