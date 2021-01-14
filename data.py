# class used to store constants and other stuff

from functools import cached_property
from glob import glob


class Data:
    __OWNER_IDS = [550555135869190158]

    @staticmethod
    def get_owners():
        return Data.__OWNER_IDS

    __channels = {"stdout": 784749132073533450,
                  "the test room": 784734923415486474,
                  "commands": 784748369507385354,
                  "bot bugs": 787276521428615178,
                  "online log": 798124127433130004}

    @staticmethod
    def get_channel(name):
        if name not in Data.__channels:
            raise NameError(f"name {name} not found in channels dictionary")
        return Data.__channels[name]

    __GUILD = 784393032245575721

    @staticmethod
    def get_guild():
        return Data.__GUILD

    __BOTS = ["Providence"]

    @staticmethod
    def get_bots():
        return Data.__BOTS

    @staticmethod
    def get_help_embeds(master):
        embeds = {}
        embeds["Providence"] = master.get_embed()
        return embeds


    pass
