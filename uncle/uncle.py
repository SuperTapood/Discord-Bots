from core import Framework, Data


class Uncle(Framework):
    def __init__(self):
        super().__init__("uncle")
        self.set_callback("on_ready", self.ready)
        return

    async def ready(self):
        print("ready")
        await self.set_presence("game", "with billion dollar hedge funds")
        chosen = Data.get_one_liner()
        # await self.send("online log", chosen.replace("%", "Rich Uncle Pennybags"))
        return

    pass
