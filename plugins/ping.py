# https://huzunluartemis.github.io/NobetciEczaneRobot/

import time
from pyrogram import Client, filters
from helper_funcs.auth_user_check import AuthUserCheck
from helper_funcs.force_sub import ForceSub
from pyrogram.types.messages_and_media.message import Message

@Client.on_message(filters.command("ping"))
def ping(_, message:Message):
    if not AuthUserCheck(message): return
    if ForceSub(message) == 400: return
    start_time = int(round(time.time() * 1000))
    reply = message.reply_text("Ping")
    end_time = int(round(time.time() * 1000))
    reply.edit_text(f"Pong\n{end_time - start_time} ms")
