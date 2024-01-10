import rubpy

class GetChannelAllMembers:
    async def get_channel_all_members(
            self: "rubpy.Client",
            channel_guid: str,
            search_text: str='',
            start_id: str=None,
    ):
        return await self.builder('getChannelAllMembers',
                                  input={
                                      'channel_guid': channel_guid,
                                      'search_text': search_text,
                                      'start_id': start_id,
                                  })