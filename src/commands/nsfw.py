import requests
import random
import traceback
from src.utils.schedule import Scheduler
from discord.ext import commands

DEFAULT_INTERVAL = 120

# JESUS PICS
LUL_TYPES = [
    "https://i.ytimg.com/vi/UnOxbQs4fnQ/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLDtZ6dp7gD0bkao5ci6TlxoFGGLDg",
    "https://www.youtube.com/watch?v=mGH9tBvcseM"
]

HENTAI_TYPES = [
    "hmidriff", "hentai", "holo", "hneko", 
    "kemonomimi", "hass", "hanal", "hthigh", "hboobs", 
    "tentacle"
]

PORN_TYPES = [
    "pgif", "4k", 
    "anal", "gonewild", "ass", 
    "pussy", "thigh", "boobs", 
]

class NsfwCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.setup_schedule = [] # stop functions

    def fetch_image(self, type):
        try:
            url = f"https://nekobot.xyz/api/image?type={type}"
            print(f"searching image type: {type}, url: {url}")
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200:
                if data["success"] == True:
                    return data["message"]
        except Exception as e:
            print(f"error: {e}")
            traceback.print_exc()

        return None

    def get_nsfw_image(self, genre):
        TYPE = PORN_TYPES if genre == "porn" else HENTAI_TYPES
        type = TYPE[random.randint(0, len(TYPE) - 1)]
        if not type:
            print("type not found", type)
            return None
        image = self.fetch_image(type)
        return image

    @commands.command(name="stop_setup")
    async def stop_setup(self, ctx: commands.Context):
        channel = ctx.message.channel
        """
            para de receber as imagens automaticamente
        """
        for f in self.setup_schedule:
            f()

        self.setup_schedule = []

        await channel.send('":+1"')

    @commands.command(name="setup")
    async def setup(self, ctx: commands.Context):
        """
            esse comando serve para configurar qual canal vai receber as imagens automaticamente
        """
        channel = ctx.message.channel
        genre = ctx.message.content.split(" ")[1]

        if genre not in ["porn", "hentai"]:
            await ctx.send("escolha entre 'porn' ou 'hentai'") # invalid genre
            return
        
        async def send():
            try:              
                image = self.get_nsfw_image(genre)
                if not image:
                    await ctx.send("nao encontrei a imagem") # image not found
                    return

                await channel.send(image)
            except Exception as e:
                print(f"error: {e}")
                traceback.print_exc()

        schedule = Scheduler(send, DEFAULT_INTERVAL)
        self.setup_schedule.append(schedule.stop_scheduler)

        await schedule.start()

    @commands.command(name="nsfw")
    async def nsfw(self, ctx: commands.Context):
        """
            envia uma imagem aleatoria nsfw
        """
        image = self.get_nsfw_image("porn")
        if not image:
            await ctx.send("nao encontrei a imagem") # image not found

        await ctx.send(image)

    @commands.command(name="hentai")
    async def hentai(self, ctx: commands.Context):
        """
            envia uma imagem aleatoria de hentai
        """
        image = self.get_nsfw_image("hentai")
        if not image:
            await ctx.send("nao encontrei a imagem") # image not found

        await ctx.send(image)

async def setup(bot: commands.Bot):
    await bot.add_cog(NsfwCommands(bot))
    print("Setup completed [NSFW]")