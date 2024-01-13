import rubpy

class JoinChannelAction:
    async def join_channel_action(
            self: "rubpy.Client",
            channel_guid: str,
            action: str = 'Join',
    ):
        if action not in ["Join", "Remove", "Archive"]:
            raise ValueError('The `action` argument can only be in `["Join", "Remove", "Archive"]`.')

        return await self.builder('joinChannelAction',
                                  input={'channel_guid': channel_guid,
                                         'action': action})