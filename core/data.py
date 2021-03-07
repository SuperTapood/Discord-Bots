# class used to store constants and make them read only
from random import randint


class Data:
    __OWNER_IDS = 550555135869190158

    @classmethod
    def get_owners(cls):
        """
        get the owners of the discord server\n
        :return: list[int], a list of the owners' id
        """
        return [cls.__OWNER_IDS]

    __channels = {"stdout": 784749132073533450,
                  "the test room": 784734923415486474,
                  "commands": 784748369507385354,
                  "bot bugs": 787276521428615178,
                  "online log": 798124127433130004}

    @classmethod
    def get_channel(cls, name):
        """
        return the id of a channel\n
        :param name: str, the name of the channel
        :return: int, the channel's id
        """
        if name not in cls.__channels:
            raise NameError(f"name {name} not found in channels dictionary")
        return cls.__channels[name]

    __GUILD = 784393032245575721

    @classmethod
    def get_guilds(cls) -> int:
        """
        a getter for the guild id\n
        :return: int, the guild id
        """
        return cls.__GUILD

    __BOTS = ["Providence", "Jack", "House", "Rich Uncle Pennybags"]

    @classmethod
    def get_bots(cls):
        """
        return a list of all the bots in the server\n
        :return: list[str], the bots
        """
        return cls.__BOTS

    @classmethod
    def get_help_embeds(cls, frame):
        """
        get the embeds for the help command \n
        :param frame: Framework, any bot that has inherits from Framework
            and has the generate_embed method
        :return: dict[string, Embed] the list of help for each bot
        """
        # frame has a dict with bots and their commands
        # omg what have i done
        return {
            bot: [
                (
                    cmd,
                    cls.get_documentation(cmd),
                    i % 2 == 0
                )
                for i, cmd in enumerate(frame.docs[bot])
            ] for bot in frame.docs
        }

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
    def get_one_liner(cls):
        """
        get a one liner for a bot\n
        :return: string, the one liner
        """
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
        """
        get the documentation for a specific command\n
        :param cmd: string, the name of the command
        :return: string, the documentation of the command
        """
        return cls.__DOC[cmd]

    __ROLES = {
        "God In The Flesh": 787272108207767553,
        "Bot Overlords": 799221802961207297,
        "QA Testers": 787370559482757180,
        "Fresh Meat": 787720125495115836
    }

    @classmethod
    def get_role(cls, role):
        """
        get a specific role id\n
        :param role: str, the role name
        :return: int, the role's id
        """
        if role in cls.__ROLES:
            return cls.__ROLES[role]
        else:
            raise NameError(f"role {role} not found in roles dictionary")

    pass
