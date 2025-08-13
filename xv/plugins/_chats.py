#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2019-2025 (c) Randy W @xtdevs, @xtsea
#
# from : https://github.com/TeamKillerX
# Channel : @RendyProjects
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import os
import time

from pyrogram import *
from pyrogram.errors import *
from pyrogram.types import *
from Ryzenth import RyzenthTools

from config import *
from logger import LOGS

rt = RyzenthTools()

@Client.on_message(
    ~filters.scheduled
    & filters.command(["start"])
    & ~filters.forwarded
)
async def startbot(m: Message):
    buttons = [
        [
            InlineKeyboardButton(
                text="Developer",
                url=f"https://t.me/xtdevs"
            )
        ]
    ]
    await m.reply_text(
        text="Welcome I'm excited to get started as a Chatbot Ryzenth bot!",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_message(
    filters.private
    & filters.command(["gptoss"])
    & ~filters.forwarded
)
async def _ask_reason(c: Client, m: Message):
    if len(m.command) > 1:
        prompt = m.text.split(maxsplit=1)[1]
    elif m.reply_to_message:
        prompt = m.reply_to_message.text
    else:
        return await m.reply_text("?")
    await c.send_chat_action(m.chat.id, enums.ChatAction.TYPING)
    await asyncio.sleep(1.5)
    try:
        start = time.monotonic()
        try:
            response = await asyncio.wait_for(
                rt.aio.chat.ask(prompt, turbo_fast=True),
                timeout=10
            )
        except asyncio.TimeoutError:
            return await m.reply_text("⚠️ Chat backend timed out. Please try again later.")
        _ = await response.to_obj()
        chat_reasoning = _.data.choices[0].message.reasoning
        chat_answer = _.data.choices[0].message.content
        elapsed = time.monotonic() - start
        if len(chat_answer) > 4096:
            with open("chat.txt", "w+", encoding="utf8") as out_file:
                out_file.write(chat_answer)
            await m.reply_document(
                document="chat.txt",
                caption=f"💡Reasoning (took {elapsed:.2f}s):\n"
                        f"<blockquote expandable>{chat_reasoning}</blockquote>"
            )
            os.remove("chat.txt")
        else:
            await m.reply_text(
                f"💡Reasoning (took {elapsed:.2f}s):\n"
                f"<blockquote expandable>{chat_reasoning}</blockquote>\n"
                f"{chat_answer}"
            )
        await c.send_chat_action(m.chat.id, enums.ChatAction.CANCEL)
        return
    except Exception as e:
        return await m.reply_text(f"Error: {e}")

@Client.on_message(
    filters.private
    & filters.command(["ask"])
    & ~filters.forwarded
)
async def _ask(c: Client, m: Message):
    if len(m.command) > 1:
        prompt = m.text.split(maxsplit=1)[1]
    elif m.reply_to_message:
        prompt = m.reply_to_message.text
    else:
        return await m.reply_text("?")
    await c.send_chat_action(m.chat.id, enums.ChatAction.TYPING)
    await asyncio.sleep(1.5)
    try:
        response = await rt.aio.chat.ask(prompt)
        output = await response.to_result()
        if len(output) > 4096:
            with open("chat.txt", "w+", encoding="utf8") as out_file:
                out_file.write(output)
            await m.reply_document(document="chat.txt")
            os.remove("chat.txt")
        else:
            await m.reply_text(output)
        await c.send_chat_action(m.chat.id, enums.ChatAction.CANCEL)
        return
    except Exception as e:
        return await m.reply_text(f"Error: {e}")
