import discord
from discord.ext import commands

class Reactions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def bird(self, ctx: commands.context.Context):
        with open("reactions/bird.jpeg", "rb") as b:
            bird = discord.File(b)

        await ctx.send(file=bird)
        
    @commands.command()
    async def pansive(self, ctx: commands.context.Context):
        pansive_text = "<:pansive:1003260802557546537>"
        await ctx.send(pansive_text)

    @commands.command()
    async def devious(self, ctx: commands.context.Context):
        devious_text = "<:devious:1004560638900699186>"
        await ctx.send(devious_text)

    @commands.command()
    async def rubidance(self, ctx: commands.context.Context):
        with open("reactions/rubidance.gif", "rb") as rd:
            rubidance = discord.File(rd)
        
        await ctx.send(file=rubidance)

    @commands.command()
    async def pint(self, ctx: commands.context.Context):
        with open("reactions/pint.png", "rb") as pint_img:
            pint = discord.File(pint_img)

        await ctx.send(file=pint)

    @commands.command()
    async def pill(self, ctx: commands.context.Context):
        with open("reactions/pills.jpg", "rb") as pills_img:
            pills = discord.File(pills_img)

        await ctx.send(file=pills)

def setup(bot: commands.Bot):
    bot.add_cog(Reactions(bot))