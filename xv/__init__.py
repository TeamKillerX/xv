import asyncio
import logging
import time

import pyrogram
from pyrogram import Client
from pyrogram.errors import *
from pyrogram.raw.all import layer

from config import API_HASH, API_ID, BOT_TOKEN
from logger import LOGS


class ChatbotRyzenth(Client):
    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()

        super().__init__(
            "chatbot_ryzenth",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=300,
            plugins=dict(root="xv.plugins"),
            sleep_threshold=180,
        )
    async def start(self):
        try:
            await super().start()
        except FloodWait as e:
            LOGS.info(e)
            await asyncio.sleep(e.value)
        self.start_time = time.time()
        LOGS.info(
            "Chatbot Ryzenth running with Pyrogram v%s (Layer %s) started on @%s. Hi!",
            pyrogram.__version__,
            layer,
            self.me.username,
        )
    async def stop(self):
        try:
            await super().stop()
            LOGS.warning("Chatbot Ryzenth stopped, Bye!")
        except ConnectionError:
            LOGS.warning("Chatbot Ryzenth is already terminated")
