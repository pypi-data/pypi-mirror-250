import rubpy

class Join:
    async def join_chat(
            self: "rubpy.Client",
            chat: str,
    ):
        if chat.startswith('c0'):
            return await self.join_channel_action(chat)
        else:
            if 'joing' in chat:
                return await self.join_group(chat)
            else:
                return await self.join_channel_by_link(chat)