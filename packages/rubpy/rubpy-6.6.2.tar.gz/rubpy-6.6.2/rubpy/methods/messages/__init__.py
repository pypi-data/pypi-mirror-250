from .auto_delete_message import AutoDeleteMessage
from .create_poll import CreatePoll
from .delete_messages import DeleteMessages
from .edit_message import EditMessage
from .forward_messages import ForwardMessages
from .get_messages_by_id import GetMessagesByID
from .get_messages_interval import GetMessagesInterval
from .get_poll_option_voters import GetPollOptionVoters
from .get_poll_status import GetPollStatus
from .request_send_file import RequestSendFile
from .send_message import SendMessage
from .send_document import SendDocmuent
from .send_gif import SendGif
from .send_music import SendMusic
from .send_video import SendVideo
from .send_voice import SendVoice
from .send_photo import SendPhoto
from .set_pin_message import SetPinMessage
from .vote_poll import VotePoll


class Messages(
        AutoDeleteMessage,
        CreatePoll,
        DeleteMessages,
        EditMessage,
        ForwardMessages,
        GetMessagesByID,
        GetMessagesInterval,
        GetPollOptionVoters,
        GetPollStatus,
        RequestSendFile,
        SendMessage,
        SetPinMessage,
        VotePoll,
        SendDocmuent,
        SendGif,
        SendMusic,
        SendVideo,
        SendVoice,
        SendPhoto,
):
        pass