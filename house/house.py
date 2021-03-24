from core import Framework, Data


class House(Framework):
    def __init__(self):
        super().__init__("house")
        self.set_callback("on_ready", self.ready)
        return

    async def ready(self):
        print("ready")
        activity = Data.get_activity(self, self.name)
        await self.set_presence(activity)
        chosen = Data.one_liner
        await self.send("online log", chosen.replace("%", "Mr. House"))
        return

    pass
