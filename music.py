import discord
from discord.ext import commands
from discord.ext.commands.core import check
import youtube_dl
import pafy
from Paparser import music, playlist
import asyncio
from discord import FFmpegPCMAudio, PCMVolumeTransformer

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}
        self.names_queue = {}

        self.setup()

    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []
            self.names_queue[guild.id] = []
            
            
    async def search_song(self, song):
        song = music(song)
        return song

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            if not ctx.voice_client.is_playing():
                ctx.voice_client.stop()
                await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
                self.song_queue[ctx.guild.id].pop(0)
                self.names_queue[ctx.guild.id].pop(0)

    async def play_song(self, ctx, *song):
        url = "".join(song)
        song = pafy.new(url)
        audio = song.getbestaudio()
        player = FFmpegPCMAudio(audio.url, **ffmpeg_options)
        ctx.voice_client.play(player, after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
        await ctx.send(f'Now playing: {song.title}')


    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("You're not connected to a voice channel")

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            self.song_queue[ctx.guild.id].clear()
            self.names_queue[ctx.guild.id].clear()
            return await ctx.voice_client.disconnect()

        await ctx.send("I'm not connected to a voice channel")


    @commands.command()
    async def lnc(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()
        await ctx.send("I'm not connected to a voice channel")

    @commands.command(aliases=['p'])
    async def play(self, ctx, *url):
        url = " ".join(url)
        print(url)

        if url is None or url == '' or url == " ":
            return await ctx.send("You must include a song to play")

        if ctx.voice_client is None:
            await self.join(ctx)

        if ("youtube.com/playlist?" in url):
            ids = playlist(url)
            for i in ids:
                self.song_queue[ctx.guild.id].append(i)
                song_name = pafy.new(i)
                song_name = song_name.title
                self.names_queue[ctx.guild.id].append(song_name)
            await ctx.send("Added to queue")
            return await self.check_queue(ctx)

        if not("youtube.com/watch?" in url or "https://youtu.be/" in url):
            await ctx.send("Searching for song")

            url = await self.search_song(url)

        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            queue_len = len(self.song_queue[ctx.guild.id])
            self.song_queue[ctx.guild.id].append(url)
            url = "".join(url)
            song_name = pafy.new(url)
            song_name = song_name.title
            self.names_queue[ctx.guild.id].append(song_name)
            return await ctx.send(f"{song_name} added to queue at position: {queue_len+1}")
        
        await self.play_song(ctx, url)

        


    @commands.command(aliases=["q"])
    async def queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("There are currently no songs in the queue")

        embed = discord.Embed(title="Song Queue", description="", colour=discord.Colour.dark_gold())
        i = 1
        for url in self.names_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"

            i += 1

        embed.set_footer(text="Bruh")
        await ctx.send(embed=embed)


    @commands.command(aliases=['s'])
    async def skip(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I'm not playing any song")

        if ctx.author.voice is None:
            return await ctx.send("You're not connected to voice channel")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("I'm not currently playing any songs for you")

        ctx.voice_client.stop()
        await self.check_queue(ctx)


    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I'm not connected to te voice chat")

        if ctx.author.voice is None:
            return await ctx.send("You're not connected to voice channel")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("I'm not currently paused any songs for you")

        if not (ctx.voice_client.is_playing()):
            return await ctx.send("I'm not currently paused any song")
        else:
            ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I'm not connected to te voice chat")

        if ctx.author.voice is None:
            return await ctx.send("You're not connected to voice channel")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("I'm not currently paused any songs for you")

        if ctx.voice_client.is_playing():
            return await ctx.send("The song is already playing")
        else:
            ctx.voice_client.resume()

    @commands.command()
    async def бебра(self, ctx):
        return await ctx.send(f"{ctx.message.author.mention} сам ты бе... бебр... иди нахуй короче")
        


ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
    }
