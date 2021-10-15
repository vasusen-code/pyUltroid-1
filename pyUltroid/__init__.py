# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import time
from re import findall

from telethon import connection

from .configs import Var
from .startup import *
from .startup.BaseClient import UltroidClient
from .startup.connections import (
    RedisConnection,
    session_file,
    vc_connection,
    where_hosted,
)
from .startup.funcs import autobot

start_time = time.time()

HOSTED_ON = where_hosted()

udB = RedisConnection(
    host=Var.REDIS_URI or Var.REDISHOST,
    password=Var.REDIS_PASSWORD or Var.REDISPASSWORD,
    port=Var.REDISPORT,
    platform=HOSTED_ON,
    decode_responses=True,
    socket_timeout=5,
    retry_on_timeout=True,
)
if udB.ping():
    LOGS.info("Connected to Redis Database")

if udB.get("TG_PROXY"):
    try:
        _proxy = findall("\\=([^&]+)", udB.get("TG_PROXY"))
        ultroid_bot = UltroidClient(
            session_file(),
            api_id=Var.API_ID,
            api_hash=Var.API_HASH,
            udB=udB,
            connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
            proxy=(_proxy[0], int(_proxy[1]), _proxy[2]),
            base_logger=TeleLogger,
        )
    except:
        ultroid_bot = UltroidClient(
        session_file(),
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        udB=udB,
        base_logger=TeleLogger,
    )
        LOGS.warning("MTProxy not supported")
else:
    ultroid_bot = UltroidClient(
        session_file(),
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        udB=udB,
        base_logger=TeleLogger,
    )

ultroid_bot.run_in_loop(autobot())

asst = UltroidClient(
    None,
    api_id=Var.API_ID,
    api_hash=Var.API_HASH,
    bot_token=udB.get("BOT_TOKEN"),
    udB=udB,
    base_logger=TeleLogger,
)

vcClient = vc_connection(udB, ultroid_bot)

if not udB.get("SUDO"):
    udB.set("SUDO", "False")

if not udB.get("SUDOS"):
    udB.set("SUDOS", "")

if not udB.get("BLACKLIST_CHATS"):
    udB.set("BLACKLIST_CHATS", "[]")

HNDLR = udB.get("HNDLR") or "."
DUAL_HNDLR = udB.get("DUAL_HNDLR") or "/"
SUDO_HNDLR = udB.get("SUDO_HNDLR") or HNDLR
