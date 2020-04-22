#ported from Uniborg @eve_enryu

from telethon import events
from userbot import CMD_HELP
from userbot.events import register
import asyncio

@register(outgoing=True, pattern="^.hacc(?: |$)(.*)")

async def _(event):
    if event.fwd_from:
        return
    animation_interval = 2
    animation_ttl = range(0, 11)
    input_str = event.pattern_match.group(1)
    if input_str == "hack":
        await event.edit(input_str)
        animation_chars = [
            "`Connecting To Hacked Private Server...`",
            "`Target Selected.`",
            "`Hacking... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Hacking... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Hacking... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",    
            "`Hacking... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Hacking... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Hacking... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Hacking... 84%\n█████████████████████▒▒▒▒ `",
            "`Hacking... 100%\n█████████HACKED███████████ `",
            "`Targeted Account Hacked...\n\nPay 6969$ To this Nigga @eve_enryu To Remove This Hack`"]
for i in animation_ttl:
await asyncio.sleep(animation_interval)
await event.edit(animation_chars[i % 11])
            
            
CMD_HELP.update({
    'hacc':
    ".hacc \
    \nUsage : LoL"})
