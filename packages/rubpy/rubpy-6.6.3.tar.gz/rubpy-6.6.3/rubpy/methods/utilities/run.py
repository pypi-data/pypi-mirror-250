from typing import Optional, Coroutine

import asyncio
import rubpy


class Run:
    def run(self: "rubpy.Client", main: Optional[Coroutine] = None, phone_number: str = None):
        async def main_runner():
            await self.start(phone_number=phone_number)
            await self.connection.get_updates()

        self.loop = asyncio.new_event_loop()

        if main:
            self.loop.run_until_complete(main)

        self.loop.run_until_complete(main_runner())