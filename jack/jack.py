from core import Framework, Data


class Jack(Framework):
    def __init__(self):
        super().__init__("jack")
        self.set_callback("on_ready", self.ready)
        return

    async def ready(self):
        print("ready")
        activity = Data.get_activity(self, self.name)
        await self.set_presence(activity)
        chosen = Data.one_liner
        await self.send("online log", chosen.replace("%", self.name))
        return

    pass


Jack().run()
