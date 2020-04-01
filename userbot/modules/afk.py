# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module which contains afk-related commands """

from random import choice, randint
from asyncio import sleep
from datetime import datetime

import asyncio
import datetime

from telethon import events
from telethon.tl import functions, types
from telethon.events import StopPropagation

from userbot import (AFKREASON, COUNT_MSG, CMD_HELP, ISAFK, BOTLOG,
                     BOTLOG_CHATID, USERS, PM_AUTO_BAN)
from userbot.events import register

try:
    from userbot.modules.sql_helper.globals import gvarstatus, addgvar, delgvar
    afk_db = True
except AttributeError:
    afk_db = False

# ========================= CONSTANTS ============================
AFKSTR = [
    "I'm in isekai rn,don't disturb me !",
]

now = datetime.datetime.now()
datime_since_afk = now
time = float(datime_since_afk.second)
days = time // (24 * 3600)
time = time % (24 * 3600)
hours = time // 3600
time %= 3600
minutes = time // 60
time %= 60
second = time
if days == 1:
    afk_since = "**Yesterday**"
elif days > 1:
    if days > 6:
        date = now + \
            datetime.timedelta(
                days=-days, hours=-hours, minutes=-minutes)
        afk_since = date.strftime("%A, %Y %B %m, %H:%I")
    else:
        wday = now + datetime.timedelta(days=-days)
        afk_since = wday.strftime('%A')
elif hours > 1:
    afk_since = f"`{int(hours)}h{int(minutes)}m` **ago**"
elif minutes > 0:
    afk_since = f"`{int(minutes)}m{int(second)}s` **ago**"
else:
    afk_since = f"`{int(second)}s` **ago**"
#==============================================================================
@register(incoming=True, disable_edited=True)
async def mention_afk(mention):
    """ This function takes care of notifying the people who mention you that you are AFK."""
    global COUNT_MSG
    global USERS
    global ISAFK
    global AFFKREASON
    ISAFK_SQL = False
    AFKREASON_SQL = None
    if afk_db:
        ISAFK_SQL = gvarstatus("AFK_STATUS")
        AFKREASON_SQL = gvarstatus("AFK_REASON")
    EXCUSE = AFKREASON_SQL if afk_db else AFKREASON
    if mention.message.mentioned and not (await mention.get_sender()).bot:
        if ISAFK:
            now = datetime.now()
            datime_since_afk = now - afk_time  # pylint:disable=E0602
            time = float(datime_since_afk.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                afk_since = "**Yesterday**"
            elif days > 1:
                if days > 6:
                    date = now + \
                        datetime.timedelta(
                            days=-days, hours=-hours, minutes=-minutes)
                    afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afk_since = wday.strftime('%A')
            elif hours > 1:
                afk_since = f"`{int(hours)}h{int(minutes)}m` **ago**"
            elif minutes > 0:
                afk_since = f"`{int(minutes)}m{int(second)}s` **ago**"
            else:
                afk_since = f"`{int(second)}s` **ago**"
            if mention.sender_id not in USERS:
                if EXCUSE:
                    await mention.reply(f"**I'm AFK right now.** (Since {afk_since}).\
                        \nReason: `{EXCUSE}`")
                else:
                    await mention.reply(str(choice(AFKSTR)))
                USERS.update({mention.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif mention.sender_id in USERS:
                if USERS[mention.sender_id] % randint(2, 4) == 0:
                    if EXCUSE:
                        await mention.reply(f"**I'm still AFK.** (Since {afk_since}).\
                            \nReason: `{EXCUSE}`")
                    else:
                        await mention.reply(str(choice(AFKSTR)))
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(incoming=True, disable_errors=True)
async def afk_on_pm(sender):
    """ Function which informs people that you are AFK in PM """
    global ISAFK
    global AFFKREASON
    ISAFK_SQL = False
    AFKREASON_SQL = None
    if afk_db:
        ISAFK_SQL = gvarstatus("AFK_STATUS")
        AFKREASON_SQL = gvarstatus("AFK_REASON")
    global USERS
    global COUNT_MSG
    EXCUSE = AFKREASON_SQL if afk_db else AFKREASON
    if sender.is_private and sender.sender_id != 777000 and not (
            await sender.get_sender()).bot:
        if PM_AUTO_BAN:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved
                apprv = is_approved(sender.sender_id)
            except AttributeError:
                apprv = True
        else:
            apprv = True
        if apprv and (ISAFK or ISAFK_SQL):
            if sender.sender_id not in USERS:
                if EXCUSE:
                    await sender.reply(f"I'm AFK right now.\
                    \nReason: `{EXCUSE}`")
                else:
                    await sender.reply(str(choice(AFKSTR)))
                USERS.update({sender.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif apprv and sender.sender_id in USERS:
                if USERS[sender.sender_id] % randint(2, 4) == 0:
                    if EXCUSE:
                        await sender.reply(
                            f"In case you didn't notice, I'm still AFK.\
                        \nReason: `{EXCUSE}`")
                    else:
                        await sender.reply(str(choice(AFKSTR)))
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(outgoing=True, pattern="^.afk(?: |$)(.*)", disable_errors=True)
async def set_afk(afk_e):
    """ For .afk command, allows you to inform people that you are afk when they message you """
    message = afk_e.text
    string = afk_e.pattern_match.group(1)
    global ISAFK
    global AFFKREASON
    ISAFK_SQL = False
    AFKREASON_SQL = None
    if afk_db:
        ISAFK_SQL = gvarstatus("AFK_STATUS")
        AFKREASON_SQL = gvarstatus("AFK_REASON")
    if string:
        if afk_db:
            addgvar("AFK_REASON", string)
        AFKREASON = string
        await afk_e.edit(f"Going AFK!\
        \nReason: `{string}`")
    else:
        await afk_e.edit("`Goodbye Cruel World!!`")
    if BOTLOG:
        await afk_e.client.send_message(BOTLOG_CHATID, "#AFK\nYou went AFK!")
    if afk_db:
        addgvar("AFK_STATUS", True)
    ISAFK = True
    raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(notafk):
    """ This sets your status as not afk automatically when you write something while being afk """
    global COUNT_MSG
    global USERS
    global ISAFK
    global AFFKREASON
    AFKREASON_SQL = None
    ISAFK_SQL = False
    if afk_db:
        ISAFK_SQL = gvarstatus("AFK_STATUS")
        AFKREASON_SQL = gvarstatus("AFK_REASON")
    if ISAFK or ISAFK_SQL:
        if afk_db:
            delgvar("AFK_STATUS")
            delgvar("AFK_REASON")
            afk_since.replace(second=0)
        ISAFK = False
        AFKREASON = None
        if BOTLOG:
            await notafk.client.send_message(
                BOTLOG_CHATID,
                "You've recieved " + str(COUNT_MSG) + " messages from " +
                str(len(USERS)) + " chats while you were away",
            )
            for i in USERS:
                name = await notafk.client.get_entity(i)
                name0 = str(name.first_name)
                await notafk.client.send_message(
                    BOTLOG_CHATID,
                    "[" + name0 + "](tg://user?id=" + str(i) + ")" +
                    " sent you " + "`" + str(USERS[i]) + " messages`",
                )
        COUNT_MSG = 0
        USERS = {}


CMD_HELP.update({
    "afk":
    ".afk [Optional Reason]\
\nUsage: Sets you as afk.\nReplies to anyone who tags/PM's \
you telling them that you are AFK(reason).\n\nSwitches off AFK when you type back anything, anywhere.\
"
})
