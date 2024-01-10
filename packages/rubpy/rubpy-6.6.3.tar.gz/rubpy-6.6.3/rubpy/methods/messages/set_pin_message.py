from typing import Union


class SetPinMessage:
    async def set_pin_message(
            self,
            object_guid: str,
            message_id: Union[str, int],
            action: str = 'Pin'
    ):
        if action not in ('Pin', 'Unpin'):
            raise ValueError('The `action` argument can only be in `("Pin", "Unpin")`.')
        
        return await self.builder('setPinMessage',
                                  input={
                                      'object_guid': object_guid,
                                      'message': str(message_id),
                                      'action': action,
                                  })