import discord
from discord.ext import commands
from config import settings
from music import Player

activity = discord.Activity(type=discord.ActivityType.listening, name="$help")

bot = commands.Bot(command_prefix="$", activity=activity, status=discord.Status.do_not_disturb)

@bot.event
async def on_ready():
    print("Bruh")

async def setup():
    await bot.wait_until_ready()
    bot.add_cog(Player(bot))

bot.loop.create_task(setup())
bot.run(settings["token"])