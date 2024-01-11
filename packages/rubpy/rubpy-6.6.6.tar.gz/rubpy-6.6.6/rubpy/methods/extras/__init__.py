from .get_object_by_username import GetObjectByUsername
from .search_global_objects import SearchGlobalObjects
from .get_profile_link_items import GetProfileLinkItems
from .ban_member import BanMember
from .get_info import GetInfo
from .join import Join


class Exctras(
    GetObjectByUsername,
    SearchGlobalObjects,
    GetProfileLinkItems,
    BanMember,
    GetInfo,
    Join,
):
    pass