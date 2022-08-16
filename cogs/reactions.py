import os
import discord
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from discord.ext import commands

class Reactions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.reactions_dir = "reactions"

    @commands.command()
    async def bird(self, ctx: commands.context.Context):
        with open(f"{self.reactions_dir}/bird.jpeg", "rb") as b:
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
        with open(f"{self.reactions_dir}/rubidance.gif", "rb") as rd:
            rubidance = discord.File(rd)
        
        await ctx.send(file=rubidance)

    @commands.command()
    async def pint(self, ctx: commands.context.Context):
        with open(f"{self.reactions_dir}/pint.png", "rb") as pint_img:
            pint = discord.File(pint_img)

        await ctx.send(file=pint)

    @commands.command()
    async def pill(self, ctx: commands.context.Context):
        with open(f"{self.reactions_dir}/pills.jpg", "rb") as pills_img:
            pills = discord.File(pills_img)

        await ctx.send(file=pills)

    # command takes in text as arguments and 
    @commands.command()
    async def gunpoint(self, ctx: commands.context.Context):
        # do nothing if no arguments are given
        # at least one element should be in the list, ".gunpoint"
        arguments = ctx.message.content.split()

        if 1 == len(arguments):
            return
        
        # otherwise, get a list of only the arguments for the command
        arguments = arguments[1:]
        
        new_img_name = "_".join(arguments)

        img = Image.open(f"{self.reactions_dir}/guns_at_rat.png")
        I1 = ImageDraw.Draw(img)
        font = ImageFont.truetype(font=None, size=32)
        I1.text((240, 367), " ".join(arguments), font=font)

        # save new image with text
        img.save(f"{self.reactions_dir}/guns_at_{new_img_name}.png")

        with open(f"{self.reactions_dir}/guns_at_{new_img_name}.png", "rb") as gun_img:
            gun = discord.File(gun_img)
        
        await ctx.send(file=gun)

        # delete new image
        os.remove(f"{self.reactions_dir}/guns_at_{new_img_name}.png")

def setup(bot: commands.Bot):
    bot.add_cog(Reactions(bot))