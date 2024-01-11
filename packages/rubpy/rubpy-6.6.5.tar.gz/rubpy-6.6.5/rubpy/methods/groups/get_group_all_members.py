class GetGroupAllMembers:
    async def get_group_all_members(
            self,
            group_guid: str,
            search_text: str='',
            start_id: str=None,
    ):
        return await self.builder('getGroupAllMembers',
                                  input={
                                      'group_guid': group_guid,
                                      'search_text': search_text,
                                      'start_id': start_id,
                                  })