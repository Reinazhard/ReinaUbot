#Port to userbot by @yincen

import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot.events import register
from userbot import bot, CMD_HELP

@register(outgoing=True, pattern="^.savedrive(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("`Reply to files.`")
       return
    reply_message = await event.get_reply_message() 
    #if not reply_message.text:
      # await event.edit("```reply to text message```")
       #return
    chat = "@GdriveXbot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("`Reply to files`")
       return
    await event.edit("`uploading files to gdrive`")
    async with bot.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=701633982))
              await bot.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("`Please unblock @GdriveXbot  and try again`")
              return
          if response.text.startswith("Authentication"):
             await event.edit("`Please Set Your Authentication`")
          else: 
             await event.edit(f"{response.message.message}check yout files progress in @GdriveXbot")

CMD_HELP.update({
        "gdrivexbot": 
        ".savedrive \
          \nUsage:upload files to gdrive.\n"
    })
