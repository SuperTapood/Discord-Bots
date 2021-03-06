from core import Framework, Data


class Jack(Framework):
    def __init__(self):
        super().__init__("jack")
        self.set_callback("on_ready", self.ready)
        return

    async def ready(self):
        print("ready")
        await self.set_presence("game", "catch with Ethan")
        chosen = Data.get_one_liner()
        await self.send("online log", chosen.replace("%", self.name))
        return

    pass


Jack().run()
