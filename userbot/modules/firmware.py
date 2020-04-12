#created by @KeselekPermen69

import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot import bot, CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.firmware(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    phone = event.pattern_match.group(1)
    firmware = f"firmware"
    chat = "@XiaomiGeeksBot"
    await event.edit("```Processing```")
    async with bot.conversation(chat) as conv:
          try:
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=774181428))
              await bot.send_message("/firmware f'{phone}'")
              response = await response
          except YouBlockedUserError:
              await event.reply("```Unblock @XiaomiGeeksBot plox```")
              return
          if response.text.startswith("**Could not find f'{phone}' requested information!**"):
             await event.edit("```Devices not found```")
          else:
             await event.delete()
             await bot.forward_messages(event.chat_id, response.message)

CMD_HELP.update({
"Firmware":
"\nUsage : Get lastest Firmware"\
})
