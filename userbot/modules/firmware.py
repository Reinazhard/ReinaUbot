#created by @KeselekPermen69

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
    chat = "@XiaomiGeeksBot"
    firmware = f"firmware"
    await event.edit("```Processing```")
    async with bot.conversation("@XiaomiGeeksBot") as conv:
          try:
              await conv.send_message(f'/{firmware} {link}')
              await bot.send_message(chat, link)
              response = await response
          except YouBlockedUserError:
              await event.reply("```Unblock @ofoxr_bot plox```")
              return
          else:
             await event.delete()
             await bot.forward_messages(event.chat_id, response.message)



CMD_HELP.update({
"Firmware":
"\nUsage : Get lastest Firmware"\
})
