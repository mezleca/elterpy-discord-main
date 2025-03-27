# this will include all basic commands
# like ping, echo, etc...

import random
from discord.ext import commands

ELTER_IMG = "https://steamuserimages-a.akamaihd.net/ugc/2474257527210946472/CFA52BF37D9B0EC7A8C1B9305B533278F49BD872/?imw=1532&imh=2048&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true"
random_messages = ["soy professor de quimica", "el sergio ese corre metiendo noscopes xd jasjdasdjasds", "nossa y como mamas", "<@842353025904410634>", ELTER_IMG]

def id_is_valid(content: str):
    try: 
        result = int(content)
        return True
    except ValueError:
        return False

class BasicCommands(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """pong"""
        await ctx.send("Pong!")

    @commands.command(name="echo")
    async def echo(self, ctx: commands.Context, *, content):
        """test"""
        await ctx.send(content)

    @commands.command(name="clean")
    async def clean(self, ctx: commands.Context):
        """limpa todo o chat"""
        channel = ctx.message.channel

        if not channel:
            await ctx.send("not found")
            return
        
        await channel.delete()
        new_channel = await ctx.message.guild.create_text_channel(
            channel.name, 
            overwrites=channel.overwrites,
            category=channel.category, 
            position=channel.position
        )

        rand_i = random.randint(0, len(random_messages) - 1)
        rand_m = random_messages[rand_i]
        await new_channel.send(rand_m)
        
    @commands.command(name="pfp")    
    async def pfp(self, ctx: commands.Context, *, content: str = None):
        """
        pega a foto do dc do negao usando o id que vc enviar
        """
        # check if the user sent someone's id
        if content:
            if not id_is_valid(content):
                await ctx.send("tem que colocar o id galado") # invalid id
                return

            user = await self.bot.fetch_user(content)
            await ctx.send(content=f"foto do <@{user.id}>\n{user.avatar.url}")
            return

        # otherwise just send the user pfp
        await ctx.send(content=f"foto do <@{ctx.author.id}>\n{ctx.author.avatar.url}")

async def setup(bot: commands.Bot):
    await bot.add_cog(BasicCommands(bot))
    print("Setup completed [Basic]")