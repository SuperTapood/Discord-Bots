from core import Framework, Data


class Uncle(Framework):
    def __init__(self):
        super().__init__("uncle")
        self.set_callback("on_ready", self.ready)
        return

    async def ready(self):
        print("ready")
        activity = Data.get_activity(self, self.name)
        await self.set_presence(activity)
        chosen = Data.get_one_liner()
        await self.send("online log", chosen.replace("%", "Rich Uncle Pennybags"))
        return

    pass
