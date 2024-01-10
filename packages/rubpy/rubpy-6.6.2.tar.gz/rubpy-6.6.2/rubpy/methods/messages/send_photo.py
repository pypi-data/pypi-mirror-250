from typing import Union, Optional
from pathlib import Path
import rubpy

class SendPhoto:
    async def send_photo(
            self: "rubpy.Client",
            object_guid: str,
            photo: Union[Path, bytes],
            caption: Optional[str] = None,
            reply_to_message_id: Optional[str] = None,
            auto_delete: Optional[int] = None, *args, **kwargs,
    ):
        """
        Send a photo.

        Args:
            object_guid (str):
                The GUID of the recipient.

            photo (Path, bytes):
                The photo data.

            caption (str, optional):
                The caption for the photo. Defaults to None.

            reply_to_message_id (str, optional):
                The ID of the message to which this is a reply. Defaults to None.
        """

        return await self.send_message(object_guid=object_guid, message=caption, reply_to_message_id=reply_to_message_id, file_inline=photo, type='Image', auto_delete=auto_delete, *args, **kwargs)