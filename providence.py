from framework import Framework


class Providence(Framework):
    def __init__(self):
        super().__init__("providence")
        self.set_callback("on_disconnect", self.disconnected)
        self.set_callback("on_ready", self.ready)
        self.set_callback("on_message", self.message)
        return

    async def disconnected(self):
        await self.send("online log", "disconnected")
        return

    async def message(self, msg):
        if not msg.author.bot:
            content = msg.clean_content
            if "69" in content:
                await self.send(msg.channel, "nice")

    async def ready(self):
        print("READY!")
        await self.send("online log", "ready!!")
        await self.set_presence("game", "with you peasants")
        # boot up the rest of the boiz
        # empty for now.
        return

    pass
