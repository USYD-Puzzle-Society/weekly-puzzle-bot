import os
import discord
import datetime
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
    async def pills(self, ctx: commands.context.Context):
        with open(f"{self.reactions_dir}/pills.jpg", "rb") as pills_img:
            pills = discord.File(pills_img)

        await ctx.send(file=pills)

    # command takes in text as arguments and 
    @commands.command()
    async def gunpoint(self, ctx: commands.context.Context, *args):
        # if no arguments are given then just send the image template
        if not args:
            with open(f"{self.reactions_dir}/guns_at_rat.png", "rb") as template:
                image = discord.File(template)
            
            await ctx.send(file=image)
            return
        
        now = datetime.datetime.now()
        # use the current minute, second and microsecond as a way of generating random numbers for the filename
        # this just ensures that if two people use the command at similar times, the bot won't try
        # to create two files with the same name
        fn_id = str(now.minute) + str(now.second) + str(now.microsecond)
        img_filename = f"{self.reactions_dir}/{fn_id}.png"

        # default font size is 128 but decreases based on how many characters there are
        default_font_size = 128
        text = " ".join(args)

        start_box = (240, 270) # the starting coordinates of the "box" which the text will be bound by
        end_box = (600, 370)
        dist_to_mid_y = (end_box[1] - start_box[1])/2
        box_length = end_box[0] - start_box[0]

        dist_to_rat_head = 25 # the x coordinate difference to the rat head (rougly) from the start x of the box
        img = Image.open(f"{self.reactions_dir}/guns_at_rat.png")
        I1 = ImageDraw.Draw(img)
        font = ImageFont.truetype(font="fonts/Avenir Light.ttf", size=default_font_size)
        text_size = I1.textlength(text=text, font=font) # size of string in pixel
        # check if the string size is larger than the box
        if text_size > box_length:
            # decrease font size until the string fits
            amt_decrease = 0
            while text_size > box_length:
                amt_decrease += 1
                new_font_size = default_font_size - amt_decrease
                font = ImageFont.truetype(font="fonts/Avenir Light.ttf", size=new_font_size)
                text_size = I1.textlength(text=text, font=font)

            # the smaller the font, the further down the text will start
            start_y = start_box[1]
            start_y = round(start_y + (dist_to_mid_y * amt_decrease/default_font_size))
            start_box = (start_box[0], start_y)
        else:
            # the smaller the number of characters, the closer to the rat head the text will start
            start_x = start_box[0]
            start_x = round(start_box[0] + (dist_to_rat_head * 1/len(text)))
            start_box = (start_x, start_box[1])
        
        I1.text(start_box, text, font=font, stroke_width=2)

        # save new image with text
        img.save(img_filename)

        # open and send new image
        with open(img_filename, "rb") as gun_img:
            gun = discord.File(gun_img)
        
        await ctx.send(file=gun)

        # delete new image
        os.remove(img_filename)

def setup(bot: commands.Bot):
    bot.add_cog(Reactions(bot))