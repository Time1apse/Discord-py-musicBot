import discord
from discord.ext import commands
from config import settings
from music import Player

bot = commands.Bot(command_prefix="$")

@bot.event
async def on_ready():
    print("Bruh")

async def setup():
    await bot.wait_until_ready()
    bot.add_cog(Player(bot))

bot.loop.create_task(setup())
bot.run(settings["token"])