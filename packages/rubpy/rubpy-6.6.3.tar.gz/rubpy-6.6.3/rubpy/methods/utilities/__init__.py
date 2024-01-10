from .start import Start
from .connect import Connect
from .disconnect import Disconnect
from .add_handler import AddHandler
from .remove_handler import RemoveHandler
from .run import Run
from .upload import UploadFile
from .download import Download


class Utilities(
    Start,
    Connect,
    Disconnect,
    AddHandler,
    RemoveHandler,
    Run,
    UploadFile,
    Download,
):
    pass