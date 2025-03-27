import os
import asyncio
import discord
import traceback

from src.utils.downloader import Downloader
from src.utils.embed import EmbedBuilder
from discord import FFmpegPCMAudio
from discord.ext import commands

# all queues
queues = []
ELTER_IMG = "https://steamuserimages-a.akamaihd.net/ugc/2474257527210946472/CFA52BF37D9B0EC7A8C1B9305B533278F49BD872/?imw=1532&imh=2048&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true"

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

class Instance:
    def __init__(self, key: int, connection: discord.VoiceClient):
        self.key = key
        self.connection = connection
        self.limit = 16
        self.songs = []
        self.current_song = None

class Queue:
    def __init__(self, list: dict):
        self.list = list

    def get(self, key: str) -> Instance:
        return self.list.get(key) or Instance(None, None)
    
    def add(self, key: str, value: Instance) -> None:
        self.list[key] = value

queue = Queue({})

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.instance = Instance(None, None)

    async def get_song(self: any, url: str):
        
        ytdl = Downloader(url)
        audio = await ytdl.search()

        if not audio.get("url"):
            return None
        
        src = FFmpegPCMAudio(audio["url"], **FFMPEG_OPTIONS)
        return audio, src
        
    async def play_next(self, ctx: commands.Context):
        instance = queue.get(ctx.guild.id)
        
        if not instance.songs:
            await instance.connection.disconnect()
            instance.key = None
            instance.connection = None
            instance.current_song = None
            return

        next_song = instance.songs.pop(0)
        instance.current_song = next_song["data"]
        
        instance.connection.play(
            next_song["src"],
            after=lambda e: asyncio.run_coroutine_threadsafe(
                self.play_next(ctx),
                self.bot.loop
            ).result()
        )
        
        await ctx.message.reply(f"🎵 playing: {next_song['data']['title']}")

    @commands.command(name="pause")
    async def pause(self, ctx: commands.Context):
        """
        comando para pausar a musica atual
        """
        instance = queue.get(ctx.guild.id)
        
        if not instance.connection:
            await ctx.message.reply("nao tem nada tocando arrombado") # not playing
            return
        
        if instance.connection.is_playing():
            instance.connection.pause()
            await ctx.message.reply("⏸️ musica PAUsada")
        else:
            await ctx.message.reply("a musica ja ta PAUsada animal") # already paused

    @commands.command(name="resume")
    async def resume(self, ctx: commands.Context):
        """
        comando para retomar a musica pausada
        """
        instance = queue.get(ctx.guild.id)
        
        if not instance.connection:
            await ctx.message.reply("nao tem nada tocando arrombado") # not playing
            return
        
        if instance.connection.is_paused():
            instance.connection.resume()
            await ctx.message.reply("desPAUsado")
        else:
            await ctx.message.reply("a musica ja ta tocando animal") # already playing

    @commands.command(name="skip")
    async def skip(self, ctx: commands.Context):
        """
        comando para pular a musica atual
        """
        instance = queue.get(ctx.guild.id)
        
        if not instance.connection:
            await ctx.message.reply(ELTER_IMG)
            return
        
        if not instance.connection.is_playing():
            await ctx.message.reply("tem nada tocando negao") # queue is empty
            return
            
        instance.connection.stop()
        await ctx.message.reply("⏭️ pulei galado")

    @commands.command(name="queue")
    async def show_queue(self, ctx: commands.Context):
        """
        comando para mostrar a queue de musicas
        """
        instance = queue.get(ctx.guild.id)
        
        if not instance.songs and not instance.current_song:
            await ctx.message.reply("tem nada na queue negao") # queue is empty
            return
            
        embed = EmbedBuilder.create_queue_embed(instance.current_song, instance.songs)
        await ctx.message.reply(embed=embed)

    @commands.command(name="clear")
    async def clear_queue(self, ctx: commands.Context):
        """
        comando para limpar a queue de musicas
        """
        instance = queue.get(ctx.guild.id)
        
        if not instance.connection:
            await ctx.message.reply("nao tem nada na queue nao galado") # queue is empty
            return
            
        # reset the queue
        instance.songs.clear()
        instance.connection.stop()

        await ctx.message.reply("🧹 limpers!") # cleaned

    @commands.command(name="disconnect", aliases=["stop"])
    async def disconnect(self, ctx: commands.Context):
        """
        comando para desconectar o bot da call
        """
        instance = queue.get(ctx.guild.id)
        
        if not instance.connection:
            await ctx.message.reply("nao to em call nao galado!")
            return
            
        await instance.connection.disconnect()

        # reset the queue
        instance.songs.clear()
        instance.key = None
        instance.connection = None
        instance.current_song = None

        await ctx.message.reply("👋")

    @commands.command(name="play")
    async def play(self, ctx: commands.Context, *, content):
        """
        comando para dar play em alguma musica do youtube (apenas url por enquanto)
        """
        try:
            print(f"{ctx.author} used the play command in {ctx.guild}")
            if not content:
                await ctx.message.reply("cade a url galado")
                return

            voice = ctx.author.voice
            if not voice:
                print("user is not in a voice channel", voice)
                return
            
            channel = voice.channel
            if not channel: 
                return
            
            instance = queue.get(ctx.guild.id)

            # check if the bot is already in a channel
            if instance.key:

                if instance.key != None and instance.key != channel.id:
                    await ctx.message.reply("eu ja to em call burrao") # im already in a call
                    return
                    
                # check if its a playlist
                if "&list" in content:
                    
                    playlist = await Downloader.get_playlist(content)
                    if not playlist:
                        await ctx.message.reply("Invalid playlist url") 
                        return

                    for song in playlist:
                        instance.songs.append({ "data": song, "src": song["src"] })
                        
                    await ctx.message.reply(f"🎵 adicionado a queue: {playlist[0]['title']}")
                    return
                    
                audio = await self.get_song(content)

                if not audio:
                    await ctx.message.reply("Invalid song url") 
                    return
                
                instance.songs.append({ "data": audio[0], "src": audio[1] })
                await ctx.message.reply(f"🎵 adicionado a queue: {audio[0]['title']}") # playing ...
                return          
            
            try:
                # create a new connection using the FFmpegAudio thing
                audio = await self.get_song(content)

                if not audio:
                    await ctx.message.reply("Invalid song url") 
                    return

                connection = await channel.connect()
         
                # play and create a lambda to run after the audio finishes
                connection.play(
                    audio[1],
                    after=lambda e: asyncio.run_coroutine_threadsafe(
                        self.play_next(ctx),
                        self.bot.loop
                    ).result()    
                )

                # save the connection to the current instance and save the instance to the queue system (1 per server)
                # instance: (key: channel_id) | (value: connection) -> queue: (key: server_id, instance)
                instance.key = channel.id
                instance.connection = connection
                instance.current_song = audio[0]

                queue.add(ctx.guild.id, instance)

                await ctx.message.reply(f"🎵 playing: {audio[0]['title']}")
                print(f"playing {audio[0]['title']} !!")
            except discord.ClientException as e:
                await ctx.send(f"erro ao conectar: {str(e)}") # could not connect to voice channel
            except Exception as e:
                await ctx.send(f"internal error: {str(e)}")
                     
        except Exception as e:
            print(e)
            traceback.print_exc()

async def setup(bot: commands.Bot):
    await bot.add_cog(MusicCommands(bot))
    print("Setup completed [MUSIC]")
