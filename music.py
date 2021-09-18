import discord
from discord.ext import commands
import youtube_dl
import pafy
from Paparser import music
import asyncio

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}

        self.setup()

    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []

    async def search_song(self, song):
        a = music(song)
        return a

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            ctx.voice_client.stop()
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def play_song(self, ctx, *song):
        player = await YTDLSource.from_url(song, stream=True) 
        ctx.voice_client.play(player, after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))


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
            return await ctx.voice_client.disconnect()

        await ctx.send("I'm not connected to a voice channel")

    @commands.command(aliases=['p'])
    async def play(self, ctx, *url):
        url = " ".join(url)
        print(url)

        if url is None:
            return await ctx.send("You must include a song to play")

        if ctx.voice_client is None:
            await self.join(ctx)

        if not("youtube.com/watch?" in url or "https://youtu.be/" in url):
            await ctx.send("Searching for song")

            url = await self.search_song(url)
            

        if ctx.voice_client.is_playing():
            queue_len = len(self.song_queue[ctx.guild.id])

            self.song_queue[ctx.guild.id].append(url)
            return await ctx.send(f"Added to queue at position: {queue_len+1}")


        await self.play_song(ctx, url)
        await ctx.send(f'Now playing: {url}')


    @commands.command(aliases=["q"])
    async def queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("There are currently no songs in the queue")

        embed = discord.Embed(title="Song Queue", description="", colour=discord.Colour.dark_gold())
        i = 1
        for url in self.song_queue[ctx.guild.id]:
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
        url = "".join(url)
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
