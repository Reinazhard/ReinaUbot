#created by @eve_enryu

import datetime
import asyncio
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot import bot, CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.ofox(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    chat = "@ofoxr_bot"
    await event.edit("```Processing```")
    async with bot.conversation(chat) as conv:
          try:
              await event.get_reply_message() 
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=1111224224))
              await asyncio.sleep(2)
              await conv.send_message(f'/{link}')
              response = conv.get_response()
          except YouBlockedUserError:
              await event.reply("```Unblock @ofoxr_bot plox```")
              return
          else:
             await event.edit(f"{response.message}")

@register(outgoing=True, pattern="^.ofoxlist(?: |$)(.*)")
async def _(event):
    chat = "@ofoxr_bot"
    link = event.pattern_match.group(1)
    await event.edit("```Processing```")
    async with bot.conversation("@ofoxr_bot") as bot_conv:
        try:
            reply_message = await event.get_reply_message()
            response = conv.wait_event(events.NewMessage(incoming=True,from_users=1111224224))            
            await conv.send_message('/list')
            await bot.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @ofoxr_bot plox```")
            return
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message.message)


CMD_HELP.update({
"ofox":
".ofox <device> \
\nUsage: Get latest OFRP\n"
".ofoxlist\
\nUsage: Get supported devices list"})
