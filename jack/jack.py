from util.framework import Framework
from util.data import Data
from util.override import override


class Jack(Framework):
    def __init__(self):
        super().__init__("Jack")
        self.set_callback("on_ready", self.ready)
        return
    
    async def ready(self):
        print("JACK!!")
        chosen = Data.get_one_liner()
        await self.send("online log", chosen.replace("%", self.name))
        return

    @override(Framework)
    def setup(self):
        self.load_extension("jackCog")
        print("JackCog loaded")
        return
    pass
