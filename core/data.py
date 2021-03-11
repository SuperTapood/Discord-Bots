# class used to store constants and make them read only
from random import randint


class Data:
    # a list of activities bots can pool from
    __ACTIVITIES = {
        "house": [
            ("game", "and always winning"),
        ],
        "jack": [
            ("game", "catch with Ethan")
        ],
        "providence": [
            ("game", "with you peasants")
        ],
        "uncle": [
            ("game", "with billion dollar hedge funds"),
            ("listen", "to the cries of the poor")
        ]
    }

    def get_activity(self, frame, name):
        """
        get and create an activity for a framework\n
        :param frame: Framework, the bot asking for an activity
        :param name: str, the name of the bot
        :return: Activity, the chosen activity
        """
        chosen = self.__ACTIVITIES[name].pop(randint(0, len(self.__ACTIVITIES[name]) - 1))
        act_type, name = chosen[0], chosen[1]
        return frame.create_activity(act_type, name, kwargs=chosen[1:])

    __BOTS = ["Providence", "Jack", "House", "Rich Uncle Pennybags"]

    __CHANNELS = {"stdout": 784749132073533450,
                  "the test room": 784734923415486474,
                  "commands": 784748369507385354,
                  "bot bugs": 787276521428615178,
                  "online log": 798124127433130004}

    __DOC = {
        "help": "Provides documentation to the provided bot,\n"
                "or all of them when none are provided",
        "userinfo": "Provides info about the provided user,\n"
                    "or the sender when none are provided",
        "on_member_join": "The bot will greet any new members\n"
                          "of the server without being invoked",
        "bj": "The bot will start to play 21 with you.\n"
              "while playing, use commands hit and skip to \n"
              "get more cards or skip the turn accordingly",
        "init": "creates a new profile for the player. This is\n"
                "required for the game to work",
        "stats": "prints out the stats for the player",
        "browse": "shows the catalog for the player",
        "buy": "upgrades a specific mine level"
    }

    __GUILD = 784393032245575721

    def get_help_embeds(self, frame):
        """
        get the embeds for the help command \n
        :param frame: Framework, any bot that has inherits from Framework
            and has the generate_embed method
        :return: dict[string, Embed] the list of help for each bot
        """
        # frame has a dict with bots and their commands
        # omg what have i done
        return {
            bot: frame.generate_embed(
                title=f"{bot}",
                fields=[
                    (
                        cmd,
                        self.get_documentation(cmd),
                        True
                    )
                    for i, cmd in enumerate(frame.docs[bot])
                ]) for bot in frame.docs
        }

    __ONE_LINERS = [
        "A wild % appeared!",
        "% reporting for duty!",
        "% is up and running!",
        "% is as high as a kite!",
        "It's a me! %!",
        "% is as ready as they'll ever be!",
        "% thinks reading this is not the best use of time",
    ]

    __OWNER_IDS = [550555135869190158]

    __ROLES = {
        "God In The Flesh": 787272108207767553,
        "Bot Overlords": 799221802961207297,
        "QA Testers": 787370559482757180,
        "Fresh Meat": 787720125495115836,
    }

    def __getattr__(self, item):
        """
        a better fetcher for data\n
        :param item: str, the item to fetch
        :return: Anything at all
        """
        if item == "owners":
            return self.__OWNER_IDS
        elif item == "roles":
            return self.__ROLES
        elif item in self.__ROLES:
            return self.__ROLES[item]
        elif item == "one_liner":
            return self.__ONE_LINERS.pop(
                randint(0, len(self.__ONE_LINERS) - 1))
        elif item == "guild":
            return self.__GUILD
        elif item == "channels":
            return self.__CHANNELS
        elif item in self.__CHANNELS:
            return self.__CHANNELS[item]
        elif item in self.__DOC:
            return self.__DOC
        elif item == "bots":
            return self.__BOTS
        raise AttributeError(f"'Data' object has no attribute {item}")

    pass
