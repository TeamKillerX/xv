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
from database import db
from logger import LOGS

rt = RyzenthTools()
gem = RyzenthTools(GEMINI_API_KEY)

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

@Client.on_message(
    filters.incoming
    & filters.text
    & filters.private
    & ~filters.command(["start", "ask", "gptoss"])
)
async def _multi_turn_gemini(client: Client, message: Message):
    if message.text:
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        await asyncio.sleep(1.5)
        query = message.text.strip()
        try:
            if not GEMINI_API_KEY:
                return await message.reply_text("401 Unauthorized LOL 😂")
            user_data = await db.backup_gemini.find_one({"user_id": message.from_user.id})
            backup_history = user_data.get("history_chat", []) if user_data else []
            backup_history.append({"role": "user", "content": query})
            response = await gem.aio.gemini_chat.ask(backup_history)
            chat = await response.to_obj()
            await message.reply_text(chat.choices[0].message.content)
            backup_history.append({"role": "assistant", "content": chat.choices[0].message.content})
            await db.backup_gemini.update_one(
                {"user_id": message.from_user.id},
                {"$set": {"history_chat": backup_history}},
                upsert=True
            )
            return
        except Exception as e:
            LOGS.error(f"Error: message.text: {str(e)}")
            return await message.reply_text("Error try again Gemini")
