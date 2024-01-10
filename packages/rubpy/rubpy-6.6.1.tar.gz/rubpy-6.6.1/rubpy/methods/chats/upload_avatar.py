class UploadAvatar:
    async def upload_avatar(
            self,
            object_guid: str,
            main_file_id: str,
            thumbnail_file_id: str,
    ):
        return await self.builder('uploadAvatar',
                                  input={
                                      'object_guid': object_guid,
                                      'main_file_id': main_file_id,
                                      'thumbnail_file_id': thumbnail_file_id,
                                  })