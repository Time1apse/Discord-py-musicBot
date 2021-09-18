
import discord
from discord.ext import commands, tasks
from config import settings
from discord import FFmpegPCMAudio
import youtube_dl
import os
import Paparser as parser
import asyncio


bot = commands.Bot(command_prefix = settings['prefix'])

@bot.event
async def on_ready():
    print("bruh")

async def check_queue(ctx, rpt = not None):
    if len(queue) > 0:
        await play(ctx, queue.pop(0), rpt = not None)
    else:
        await ctx.send("Queue is empty")


ffmpeg_options = {
    'options': '-vn'
}

ytdl_opts = {
           'format': 'bestaudio/best',
           'postprocessors': [{
               'key': 'FFmpegExtractAudio',
               'preferredcodec': 'mp3',
               'preferredquality': '192',
               }],
           }

ytdl = youtube_dl.YoutubeDL(ytdl_opts)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@bot.command()
async def bruh(ctx):
    author = ctx.message.author
    await ctx.send(f'Some shit was happend, {author.mention}')

@bot.command()
async def join(ctx):
    vc = ctx.voice_client
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
    if vc == None:
        await voice.connect()


@bot.command()
async def play(ctx, *url: str, rpt = None, ):
    global queue

    vc = ctx.voice_client

    if len(url) > 0:
        url = " ".join(url)
        print(url)

        if (not (url.startswith("https://you")) and not (url.startswith("https://www.you"))):
            url = parser.music(url)

        if rpt == None:
            queue.append(url)

        if vc == None:
            pass
        else:
            if vc.is_playing():
                queue.append(url)
                await ctx.send("Added to queue")
                return

    channel = ctx.message.author.voice.channel
    
    if vc == None:
        await channel.connect()
    else:
        await vc.move_to(channel)

    server = ctx.message.guild
    voice_channel = server.voice_client


    async with ctx.typing():
        player = await YTDLSource.from_url(queue.pop(0), loop=bot.loop, stream=True) 
        ctx.voice_client.play(player, after = lambda e: bot.loop.create_task(check_queue(ctx, rpt)))

    await ctx.send(f'Now playing: {player.title}')

@bot.command()
async def queue_(ctx, *url):
    global queue

    url = " ".join(url)
    print(url)

    if (not (url.startswith("https://you")) and not (url.startswith("https://www.you"))):
        url = parser.music(url)

    queue.append(url)
    await ctx.send(f'{url} added to queue')

@bot.command()
async def remove(ctx, number):
    global queue
    
    try:
        del(queue[int(number)])
        await ctx.send(f"your queue is now '{queue}'")
    except:
        await ctx.send("Queue is either **empty** or the index is **out of range**")

@bot.command()
async def view(ctx):
    global queue
    await ctx.send(f"your queue now is '{queue}'")

@bot.command()
async def leave(ctx):
    vc = ctx.voice_client

    if not vc:
        await ctx.send("I am not in a voice channel.")
        return

    await vc.disconnect()
    await ctx.send("I have left the voice channel!")

@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice is None:
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("No audio is playing.")
    else:
        await ctx.send("I am currently not in a channel.")

@bot.command()
async def resume(ctx):
    vc = ctx.voice_client
    if vc.is_paused():
        vc.resume()
    else:
        await ctx.send("audio is not paused")

@bot.command()
async def stop(ctx):
    vc=ctx.voice_client
    vc.stop()
    queue.clear()

@bot.command()
async def skip(ctx):
    vc=ctx.voice_client
    if vc.is_playing():
        vc.stop()
        await check_queue(ctx)





bot.run(settings['token'])
