# (c) @xditya
# This file is a part of https://github.com/xditya/BotStatus

import pytz
import logging
import asyncio
from datetime import datetime as dt
from telethon.tl.functions.messages import GetHistoryRequest
from decouple import config
from telethon.sessions import StringSession
from telethon import TelegramClient

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

try:
    appid = config("3609223")
    apihash = config("302bf5498005e091fd23c88d8e76740e")
    session = config("1BVtsOKMBu4CELgingQXglIp8G7Bz2jbVJjEuL2Q94SWlVDzMqMLlVMhMVR57x6Wnbbujqq6iXHzcz940FmoGlUd4AYa0ar5TzoW4k50imPz2x7UDjg3GS0JWQa6vP_IsrlutYIN7sO9bqj7-DDFmocL6rHe3jI-tH5w0VKUxtqYIqp0YPdA7JjilSopFbuDEuFsUbuPV64RP6APG8pDFVhnbMEgeTLIGYuuTUf6XP9-w1oKWDqd9xUqoXMO63VDx06RHLJSXL6tgBj_gft4h-UdwtAT07Nl9MgpNIGBXOjqGGui2LPovAvQI_rjbz7Y__Oajc7PuKvOFV63jjTaBPRzAVJe5IuM=", default=None)
    chnl_id = config("-1001418249477", cast=int)
    msg_id = config("67075", cast=int)
    botlist = config("1769784837 1671321126 1701860498 1700456017")
    bots = botlist.split()
    session_name = str(session)
    user_bot = TelegramClient(StringSession(session_name), appid, apihash)
    print("Started")
except Exception as e:
    print(f"ERROR\n{str(e)}")

async def BotzHub():
    async with user_bot:
        while True:
            print("[INFO] starting to check uptime..")
            await user_bot.edit_message(int(chnl_id), msg_id, "**@BotzHub Bots Stats.**\n\n`Performing a periodic check...`")
            c = 0
            edit_text = "**𖤍 Λℓσηє 𖤍’s Bots’ Stats.**\n\n"
            for bot in bots:
                print(f"[INFO] checking @{bot}")
                snt = await user_bot.send_message(bot, "/start")
                await asyncio.sleep(10)

                history = await user_bot(GetHistoryRequest(
                    peer=bot,
                    offset_id=0,
                    offset_date=None,
                    add_offset=0,
                    limit=1,
                    max_id=0,
                    min_id=0,
                    hash=0
                ))
                msg = history.messages[0].id
                if snt.id == msg:
                    print(f"@{bot} is down.")
                    edit_text += f"@{bot} - ❌\n"
                elif snt.id + 1 == msg:
                    edit_text += f"@{bot} - ✅\n"
                await user_bot.send_read_acknowledge(bot)
                c += 1
                await user_bot.edit_message(int(chnl_id), msg_id, edit_text)
            k = pytz.timezone("Asia/Kolkata")
            month = dt.now(k).strftime("%B")
            day = dt.now(k).strftime("%d")
            year =  dt.now(k).strftime("%Y")
            t = dt.now(k).strftime("%H:%M:%S")
            edit_text +=f"\n**Last Checked:** \n`{t} - {day} {month} {year} [IST]`\n\n__Bots status are auto-updated every 2 hours__"
            await user_bot.edit_message(int(chnl_id), msg_id, edit_text)
            print(f"Checks since last restart - {c}")
            print("Sleeping for 2 hours.")
            await asyncio.sleep(2 * 60 * 60)

user_bot.loop.run_until_complete(BotzHub())
