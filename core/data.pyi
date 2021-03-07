# class used to store constants and make them read only

from discord import Embed

from core import Framework


class Data:
    __BOTS: list[str]

    @classmethod
    def get_bots(cls) -> list[str]:
        ...

    __channels: dict[str, int]

    @classmethod
    def get_channel(cls, name: str) -> int:
        ...

    __DOC: dict[str, str]

    @classmethod
    def get_documentation(cls, cmd: str) -> str:
        ...

    __GUILD: int

    @classmethod
    def get_guild(cls) -> int:
        ...

    @classmethod
    def get_help_embeds(cls, frame: Framework) -> dict[str, Embed]:
        ...

    __one_liners: list[str]

    @classmethod
    def get_one_liner(cls) -> str:
        ...

    __OWNER_IDS: list[int]

    @classmethod
    def get_owners(cls):
        ...

    __ROLES: dict[str, int]

    @classmethod
    def get_role(cls, role: str) -> int:
        ...

    pass
