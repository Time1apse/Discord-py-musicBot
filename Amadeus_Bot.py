import discord
from discord.ext import commands, tasks
from config import settings
from music import Player
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.core import check
import youtube_dl
import pafyfixed as pafy
from Paparser import music, playlist
import asyncio
from discord import FFmpegPCMAudio, PCMVolumeTransformer

activity = discord.Activity(type=discord.ActivityType.listening, name="$help")

bot = commands.Bot(command_prefix="$", activity=activity, status=discord.Status.do_not_disturb, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bruh")
    bot.loop.create_task(setup())


async def setup():
    await bot.wait_until_ready()
    await bot.add_cog(Player(bot))


bot.run(settings["token"])

