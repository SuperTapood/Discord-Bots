from util.framework import Framework
from util.data import Data
from util.override import override


class House(Framework):
    def __init__(self):
        super().__init__("house")
        self.set_callback("on_ready", self.ready)
        return

    @override(Framework)
    def setup(self):
        self.load_extension("cogs.houseCog")
        print("House Cog Loaded!")

    async def ready(self):
        print("HOUSE !")
        await self.set_presence("game", "and always winning")
        chosen = Data.get_one_liner()
        await self.send("online log", chosen.replace("%", "Mr. House"))
        return

    pass


House().run()
