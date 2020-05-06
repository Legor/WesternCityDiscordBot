import os
from dotenv import load_dotenv
from discord.ext import commands

from cogs import GamblingCog, GameManagementCog

# store the discord authentication token locally in the file auth.env with
# DISCORD_TOKEN=your_very_long_cryptic_token
load_dotenv('auth.env')
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!', description="This machine helps you play Western City.",)
bot.add_cog(GamblingCog(bot))
bot.add_cog(GameManagementCog(bot))


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error.args)


bot.run(TOKEN)
