from discord import Member

from core import MasterCog


class JackCog(MasterCog):

    @MasterCog.listener()
    async def on_member_join(self, member: Member) -> None:
        ...

    @MasterCog.listener()
    async def on_member_remove(self, member: Member) -> None:
        ...

    pass
