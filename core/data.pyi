from discord import Embed

from core import Framework


class Data:
    __OWNER_IDS: list[int]

    @classmethod
    def get_owners(cls: Data) -> list:
        ...

    __channels: dict[str, int]

    @classmethod
    def get_channel(cls: Data, name: str) -> int:
        ...

    __GUILD: int

    @classmethod
    def get_guilds(cls: Data) -> int:
        ...

    __BOTS: list[str]

    @classmethod
    def get_bots(cls: Data) -> list[str]:
        ...

    @classmethod
    def get_help_embeds(cls: Data, prov: Framework) -> dict[str, Embed]:
        ...

    __one_liners: list[str]

    @classmethod
    def get_one_liner(cls: Data) -> str:
        ...

    __DOC: dict[str, str]

    @classmethod
    def get_documentation(cls: Data, cmd: str):
        ...

    __ROLES: dict[str, int]

    @classmethod
    def get_role(cls: Data, role: str) -> int:
        ...

    pass
