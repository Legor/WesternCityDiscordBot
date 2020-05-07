import random
import json
from pathlib import Path

from discord.ext import commands
from discord import Embed
from objects.characters import PlayerCharacter, NonPlayerCharacter


class GamblingCog(commands.Cog, name="Gambling"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll', aliases=["r", "dice"], help='Simulates rolling dice.')
    async def roll(self, ctx, number_of_dice: int, number_of_sides: int):
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.send(', '.join(dice))


class PokerChipsCog(commands.Cog, name="Poker Chips"):

    def __init__(self, bot):
        self.bot = bot
        # available chips per player
        self.chips = {}
        # current chips in the pool
        self.pool = 0

    @commands.command(name='spend', help='Spend the given amount of chips (default 1).')
    async def spend_chip(self, ctx, amount: int=1):
        if ctx.author not in self.chips.keys():
            await ctx.send('Can\'t find chips for {}'.format(ctx.author))
        elif self.chips[ctx.author] - amount < 0:
            await ctx.send('{} only has {} chips left. Can\'t spend {} chips.'.format(ctx.author,
                                                                                      self.chips[ctx.author], amount))
        else:
            self.chips[ctx.author] -= amount
            await ctx.send('{} spend {} chips, {} left.'.format(ctx.author, amount, self.chips[ctx.author]))





class GameManagementCog(commands.Cog, name="Management"):

    def __init__(self, bot):
        self.bot = bot
        self.chips = PokerChipsCog
        self.players_list = []
        self.npc_list = []

    def save_session(self):
        with open("./session/players.json", "w") as output_file:
            json.dump([p.__dict__ for p in self.players_list], output_file)
        with open("./session/npcs.json", "w") as output_file:
            json.dump([p.__dict__ for p in self.npc_list], output_file)

    # load a list of previously stored characters
    def load_session(self):
        self.players_list.clear()
        self.npc_list.clear()
        if Path('./session/players.json').exists():
            with open("./session/players.json", "r") as read_file:
                data = json.load(read_file)
                for d in data:
                    p = PlayerCharacter()
                    p.__dict__.update(d)
                    self.players_list.append(p)
        if Path('./session/npcs.json').exists():
            with open("./session/npcs.json", "r") as read_file:
                data = json.load(read_file)
                for d in data:
                    p = NonPlayerCharacter()
                    p.__dict__.update(d)
                    self.npc_list.append(p)

    @commands.command(name='new_pc', help='Create a new player character.')
    async def add_new_player_character(self, ctx, character_name: str):
        new_player = PlayerCharacter(character_name=character_name, user=ctx.author)
        self.players_list.append(new_player)

        self.save_session()
        await ctx.send('Added {} for {}'.format(character_name, ctx.author))

    @commands.command(name='assign_pc', help='Assign an existing player character to a player.')
    #@commands.has_role('gamemaster')
    async def assign_player_character(self, ctx, character_name: str, player_name: str):
        found = False
        for p in self.players_list:
            if character_name == p.character_name:
                found = True
                p.user = player_name
                break
        if found:
            self.save_session()
            await ctx.send('Assigned {} to {}'.format(character_name, player_name))
        else:
            await ctx.send('Couldn\'t find character {}'.format(character_name))


    @commands.command(name='restart', help='Check and load a list of previously created characters.')
    #@commands.has_role('gamemaster')
    async def restart(self, ctx):
        await ctx.send('Looking for existing characters...')
        self.load_session()
        await ctx.send('Found {} characters and {} NPCs'.format(len(self.players_list), len(self.npc_list)))

    @commands.command(name='list_characters', aliases=["lc", "players"], help='Print the list of available characters.')
    async def list_characters(self, ctx):

        if len(self.players_list) < 1:
            await ctx.send('No characters loaded.')
        else:
            embed = Embed(title="Available player characters", color=0x00ff00)
            for p in self.players_list:
                embed.add_field(name=p.character_name, value="{} \n {}".format(p.user, p.friend), inline=False)
            await ctx.send(embed=embed)

    @commands.command(name='list_npcs', help='Print the list of NPCs.')
    async def list_npcs(self, ctx):
        if len(self.npc_list) < 1:
            await ctx.send('No NPCs loaded.')
        else:
            await ctx.send(', '.join([str(p) for p in self.npc_list]))





