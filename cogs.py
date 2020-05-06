import random
import json
from pathlib import Path

from discord.ext import commands
from objects.characters import PlayerCharacter


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

    def __getstate__(self):
        return ({
            'players' : self.players_list
            })
        pass

    def __setstate__(self, state_dict):
        self.players_list = state_dict['players']

    def save_session(self):
        with open("players.json", "w") as output_file:
            json.dump([p.__dict__ for p in self.players_list], output_file)

    # load a list of previously store players
    def load_session(self):
        if Path('players.json').exists():
            with open("players.json", "r") as read_file:
                data = json.load(read_file)
                for d in data:
                    p = PlayerCharacter()
                    p.__dict__.update(d)
                    self.players_list.append(p)

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





