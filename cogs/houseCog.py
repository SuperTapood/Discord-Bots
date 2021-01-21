from random import randint

from discord.ext.commands import Cog, command


class HouseCog(Cog):
    suits = {
        0: "♣",
        1: "❤",
        2: "♠",
        3: "♦"
    }
    player = []
    bot_cards = []
    player_s = []
    bot_s = []
    deck = []
    player_skip = False
    bot_skip = False
    is_playing = False

    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")
        return

    def generate_deck(self):
        self.deck = [list(range(1, 11)) for _ in range(4)]
        return

    def deal(self, cards, signs, amount):
        for _ in range(amount):
            sign = randint(0, len(self.deck) - 1)
            while not self.deck[sign]:
                if self.deck == [[], [], [], []]:
                    raise Exception("Deck is gone !")
                sign = randint(0, len(self.deck) - 1)
            value = self.deck[sign].pop(randint(0, len(self.deck[sign]) - 1))
            cards.append(value)
            signs.append(sign)
        return

    def get_cards(self, cards, signs, is_bot=False):
        out = ""
        for i, card, sign in zip(range(len(cards)), cards, signs):
            if i == 0 and is_bot:
                out += "?, "
            else:
                out += f"{card}{self.suits[sign]}, "
        return out

    async def present_cards(self, ctx):
        fields = [
            ("Bot Cards", self.get_cards(self.bot_cards, self.bot_s, True), False),
            ("Bot Sum", str(sum(self.bot_cards[1:])) + " + ?", True),
            ("Player Cards", self.get_cards(self.player, self.player_s), False),
            ("Player Sum", str(sum(self.player)), True),
        ]
        embed = self.bot.generate_embed(title="21", fields=fields)
        await ctx.send(embed=embed)
        # print("player cards", self.player)
        # print("player signs", self.player_s)
        # print("bot cards", self.bot_cards)
        # print("bot signs", self.bot_s)
        await ctx.send("What will you do? hit or h /surrender or s")
        return

    @command(name="bj")
    async def play_bj(self, ctx):
        self.is_playing = True
        await ctx.send("Starting game")
        self.generate_deck()
        self.player = []
        self.bot_cards = []
        self.player_s = []
        self.bot_s = []
        self.player_skip = False
        self.deal(self.player, self.player_s, 2)
        self.deal(self.bot_cards, self.bot_s, 2)
        await self.present_cards(ctx)
        return

    def bot_play(self):
        player_vision = self.player[1:]
        self_sum = sum(self.bot_cards)
        player_sum = sum(player_vision)
        if player_sum > 21 or self_sum >= 21:
            return True
        used_dict = {}
        for card in player_vision:
            if card not in used_dict:
                used_dict[card] = 1
            else:
                used_dict[card] += 1
        for card in self.bot_cards:
            if card not in used_dict:
                used_dict[card] = 1
            else:
                used_dict[card] += 1
        good_cards = min(21 - self_sum, 10)
        exist = good_cards * 4
        for card, value in used_dict.items():
            if card <= good_cards:
                exist -= value
        total = 40 - len(self.bot_cards) - len(self.player)
        prob = (exist / total) * 100
        return prob < 25

    @command(name="hit", aliases=["h"])
    async def hit(self, ctx):
        if self.is_playing:
            self.deal(self.player, self.player_s, 1)
            self.bot_skip = self.bot_play()
            if not self.bot_skip:
                self.deal(self.bot_cards, self.bot_s, 1)
            await self.present_cards(ctx)
        return

    @command(name="skip", aliases=["surrender", "s"])
    async def skip(self, ctx):
        if self.is_playing:
            self.player_skip = True
            self.bot_skip = self.bot_play()
            if self.bot_skip and self.player_skip:
                await self.stop(ctx)
                return
            if not self.bot_skip:
                self.deal(self.bot_cards, self.bot_s, 1)
            await self.present_cards(ctx)
        return

    async def stop(self, ctx):
        sum_player = sum(self.player)
        sum_bot = sum(self.bot_cards)
        abs_player = abs(sum_player - 21)
        abs_bot = abs(sum_bot - 21)
        await ctx.send(f"Bot sum is {sum_bot}")
        await ctx.send(f"Player sum is {sum_player}")
        if (
            sum_player > 21
            and sum_bot <= 21
            or (sum_bot <= 21 or sum_player > 21)
            and abs_player > abs_bot
        ):
            await ctx.send("Bot won!")
        elif sum_bot > 21 and sum_player <= 21 or abs_bot > abs_player:
            await ctx.send("Player won!")
        elif abs_player == abs_bot:
            await ctx.send("Draw!")
        await ctx.send("Best of 3?")
        self.is_playing = False
        return
    pass


def setup(bot):
    bot.add_cog(HouseCog(bot))
    return
