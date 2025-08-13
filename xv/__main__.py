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

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import logging
import sys
import traceback
from contextlib import closing, suppress
from datetime import datetime as dt
from datetime import timedelta

from pyrogram import idle
from uvloop import install

from database import db
from logger import LOGS

from . import ChatbotRyzenth

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram.syncer").setLevel(logging.WARNING)
logging.getLogger("pyrogram.client").setLevel(logging.WARNING)
loop = asyncio.get_event_loop()

async def shutdown(loop):
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    with suppress(asyncio.CancelledError):
        await asyncio.gather(*tasks, return_exceptions=True)
    LOGS.info("Application shutdown complete")

async def main():
    try:
        await db.connect()
        _ = ChatbotRyzenth(loop=loop)
        await _.start()
        LOGS.info("Application startup complete")
        await idle()

    except Exception as e:
        LOGS.critical(f"Fatal error: {str(e)}")
        traceback.print_exc()
    finally:
        await shutdown(asyncio.get_event_loop())

if __name__ == "__main__":
    install()
    with closing(loop):
        with suppress(asyncio.CancelledError, KeyboardInterrupt):
            loop.run_until_complete(main())

        loop.run_until_complete(asyncio.sleep(3))
        if not loop.is_closed():
            loop.close()
