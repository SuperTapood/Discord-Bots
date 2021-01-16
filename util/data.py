# class used to store constants and make them read only
from random import randint


class Data:
    __OWNER_IDS = 550555135869190158

    @staticmethod
    def get_owners() -> list:
        # get the owner of the bot
        # this is returned as a list bc discord.py needs it to
        return [Data.__OWNER_IDS]

    __channels = {"stdout": 784749132073533450,
                  "the test room": 784734923415486474,
                  "commands": 784748369507385354,
                  "bot bugs": 787276521428615178,
                  "online log": 798124127433130004}

    @staticmethod
    def get_channel(name) -> int:
        # get the id of channel 'name'
        if name not in Data.__channels:
            # this is being raised so that i'll notice that an illegal channel was entered
            raise NameError(f"name {name} not found in channels dictionary")
        return Data.__channels[name]

    __GUILD = 784393032245575721

    @staticmethod
    def get_guild() -> int:
        # a getter for the guild
        return Data.__GUILD

    __BOTS = ["Providence"]

    @staticmethod
    def get_bots() -> list:
        # a getter for all the bots this project will manage
        return Data.__BOTS

    @staticmethod
    def get_help_embeds(prov) -> dict:
        # gets all of the embeds for the help command from all of the bots
        # prov is providence, the master bot
        return {"Providence": prov.get_embed()}

    __one_liners = [
        "A wild % appeared!",
        "% reporting for duty!",
        "% is up and running!",
        "% is as high as a kite!",
        "It's a me! %!",
        "% is as ready as they'll ever be!",
        "% thinks reading this is not the best use of time",
    ]

    @staticmethod
    def get_one_liner() -> str:
        return Data.__one_liners.pop(randint(0, len(Data.__one_liners) - 1))

    pass
