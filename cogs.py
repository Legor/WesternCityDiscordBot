import random
import json
from pathlib import Path

from discord.ext import commands
from objects.characters import PlayerCharacter, NonPlayerCharacter


class GamblingCog(commands.Cog, name="Gambling"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll', help='Simulates rolling dice.')
    async def roll(self, ctx, number_of_dice: int, number_of_sides: int):
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.send(', '.join(dice))


class GameManagementCog(commands.Cog, name="Management"):

    def __init__(self, bot):
        self.bot = bot
        self.players_list = []
        self.npc_list = []

    def save_session(self):
        with open("./session/players.json", "w") as output_file:
            json.dump([p.__dict__ for p in self.players_list], output_file)
        with open("./session/npcs.json", "w") as output_file:
            json.dump([p.__dict__ for p in self.npc_list], output_file)

    # load a list of previously stored characters
    def load_session(self):
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

    @commands.command(name='new_player', help='Create a new player character.')
    async def add_new_player(self, ctx, character_name: str):
        new_player = PlayerCharacter(character_name=character_name, user=ctx.author)
        self.players_list.append(new_player)

        self.save_session()
        await ctx.send('Added {} for {}'.format(character_name, ctx.author))

    @commands.command(name='load_players', help='Load a list of previously created players.')
    async def load_player_list(self, ctx):
        self.load_session()

    @commands.command(name='list_players', help='Print the list of current players.')
    async def list_players(self, ctx):
        if len(self.players_list) < 1:
            await ctx.send('No players loaded.')
        else:
            await ctx.send(', '.join([str(p) for p in self.players_list]))

    @commands.command(name='list_npcs', help='Print the list of NPCs.')
    async def list_npcs(self, ctx):
        if len(self.npc_list) < 1:
            await ctx.send('No NPCs loaded.')
        else:
            await ctx.send(', '.join([str(p) for p in self.npc_list]))





