# class used to store constants and make them read only
from random import randint


class Data:
    __OWNER_IDS = 550555135869190158

    @classmethod
    def get_owners(cls):
        # get the owner of the bot
        # this is returned as a list bc discord.py needs it to
        return [cls.__OWNER_IDS]

    __channels = {"stdout": 784749132073533450,
                  "the test room": 784734923415486474,
                  "commands": 784748369507385354,
                  "bot bugs": 787276521428615178,
                  "online log": 798124127433130004}

    @classmethod
    def get_channel(cls, name) -> int:
        # get the id of channel 'name'
        if name not in cls.__channels:
            # this is being raised so that i'll notice that an illegal channel was entered
            raise NameError(f"name {name} not found in channels dictionary")
        return cls.__channels[name]

    __GUILD = 784393032245575721

    @classmethod
    def get_guilds(cls) -> int:
        # a getter for the guild
        return cls.__GUILD

    __BOTS = ["Providence", "Jack"]

    @classmethod
    def get_bots(cls) -> list:
        # a getter for all the bots this project will manage
        return cls.__BOTS

    @classmethod
    def get_help_embeds(cls, prov) -> dict:
        # gets all of the embeds for the help command from all of the bots
        # every two commands will be inlined
        out = {"Providence": prov.generate_embed(
            title="Help With the Providence bot",
            fields=[
                ("!help", cls.get_documentation("help"), True),
                ("!userinfo", cls.get_documentation("userinfo"), True),
            ],
        ), "Jack": prov.generate_embed(
            title="Help With the Jack bot",
            fields=[("on_member_join", cls.get_documentation("on_member_join"), True)]
        ), "Mr. House": prov.generate_embed(
            title="Help With the Mr. House bot",
            fields=[("!bj", cls.get_documentation("bj"), True)]
        )}
        return out

    __one_liners = [
        "A wild % appeared!",
        "% reporting for duty!",
        "% is up and running!",
        "% is as high as a kite!",
        "It's a me! %!",
        "% is as ready as they'll ever be!",
        "% thinks reading this is not the best use of time",
    ]

    @classmethod
    def get_one_liner(cls) -> str:
        return cls.__one_liners.pop(randint(0, len(cls.__one_liners) - 1))

    __DOC = {
        "help": "Provides documentation to the provided bot,\n"
                "or all of them when none are provided",
        "userinfo": "Provides info about the provided user,\n"
                    "or the sender when none are provided",
        "on_member_join": "The bot will greet any new members\n"
                          "of the server without being invoked",
        "bj": "The bot will start to play 21 with you.\n"
              "while playing, use commands hit and skip to \n"
              "get more cards or skip the turn accordingly"
    }

    @classmethod
    def get_documentation(cls, cmd):
        return cls.__DOC[cmd]

    __ROLES = {
        "God In The Flesh": 787272108207767553,
        "Bot Overlords": 799221802961207297,
        "QA Testers": 787370559482757180,
        "Fresh Meat": 787720125495115836
    }

    @classmethod
    def get_role(cls, role):
        if role in cls.__ROLES:
            return cls.__ROLES[role]
        else:
            raise NameError(f"role {role} not found in roles dictionary")

    pass
