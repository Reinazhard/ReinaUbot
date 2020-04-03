#created by @eve_enryu

import datetime
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
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=424466890))
              await bot.send_message(chat, link)
              response = await response
          except YouBlockedUserError:
              await event.reply("```Unblock @ofoxr_bot plox```")
              return
          else:
             await event.delete()
             await bot.forward_messages(event.chat_id, response.message)


@register(outgoing=True, pattern="^.ofoxlist(?: |$)(.*)")
async with bot.conversation(chat) as conv:
    try:
        await conv.send_message('/list')
        await bot.send_message(chat, link)
    except YouBlockedUserError:
        await event.reply("```Unblock @ofoxr_bot plox```")
        return
    else:
        await event.delete()
        await bot.forward_messages(event.chat_id, response.message)

CMD_HELP.update({
"Orange Fox Recovery Project":
".ofox <device>\
\nUsage: Get latest OFRP\n"
".ofoxlist\
\nGet supported device list"})
