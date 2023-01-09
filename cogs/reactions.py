import os
import discord
import datetime
import numpy as np
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
    async def dog(self, ctx: commands.context.Context):
        with open(f"{self.reactions_dir}/dog.jpg", "rb") as d:
            dog = discord.File(d)

        await ctx.send(file=dog)

    @commands.command()
    async def wut(self, ctx: commands.context.Context):
        with open(f"{self.reactions_dir}/wut.jpg", "rb") as w:
            wut = discord.File(w)

        await ctx.send(file=wut)

    @commands.command()
    async def stare(self, ctx: commands.context.Context):
        await ctx.send("https://tenor.com/view/bird-birds-mynah-capcut-zoom-gif-23327639")

    @commands.command(aliases=["a"*i for i in range(3, 11)])
    async def aa(self, ctx: commands.context.Context):
        with open(f"{self.reactions_dir}/laugh.gif", "rb") as laugh_gif:
            laugh = discord.File(laugh_gif)

        await ctx.send(file=laugh)
        
    @commands.command()
    async def tear(self, ctx: commands.context.Context):
        await ctx.send("https://tenor.com/view/birb-sad-crying-bird-upset-gif-22556773")

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

    @commands.command()
    async def sus(self, ctx: commands.context.Context):
        await ctx.send("https://tenor.com/view/among-us-kill-all-impostor-gif-18706928")

    # command takes in text as arguments and superimposes on top of the
    # guns pointing at rat image
    """
    Hoping to add text wrapping someday so that even longer strings can be
    placed on the image while still be legible
    """
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

    @commands.command()
    async def bonk(self, ctx: commands.context.Context, *args):
        if not args:
            with open(f"{self.reactions_dir}/bonk.jpg", "rb") as template:
                image = discord.File(template)

            await ctx.send(file=image)
            return

        now = datetime.datetime.now()
        # use the current minute, second and microsecond as a way of generating random numbers for the filename
        # this just ensures that if two people use the command at similar times, the bot won't try
        # to create two files with the same name
        fn_id = str(now.minute) + str(now.second) + str(now.microsecond)
        img_filename = f"{self.reactions_dir}/{fn_id}.jpg"

        # default font size is 128 but decreases based on how many characters there are
        default_font_size = 100
        text = " ".join(args)

        start_box = (420, 240) # the starting coordinates of the "box" which the text will be bound by
        end_box = (630, 320)
        dist_to_mid_y = (end_box[1] - start_box[1])/2
        box_length = end_box[0] - start_box[0]

        dist_to_bonked_head = 20 # the x coordinate difference to the head being bonked (rougly) from the start x of the box
        img = Image.open(f"{self.reactions_dir}/bonk.jpg")
        I1 = ImageDraw.Draw(img)

        # if the user has tagged someone with this command, put their pfp on the bonk image
        # only the first tagged user will be used
        if ctx.message.mentions:
            user = ctx.message.mentions[0]
            pfp_filename = f"{self.reactions_dir}/pfp.png"
            await user.avatar_url.save(pfp_filename)
            pfp = Image.open(pfp_filename)

            # resize image
            pfp = pfp.resize((100, 100))

            # crop image into a circle
            height, width = pfp.size
            lum_img = Image.new("L", [height, width], 0)

            draw = ImageDraw.Draw(lum_img)
            draw.pieslice([(0, 0), (height, width)], 0, 360, fill=255, outline="white")

            img_arr =np.array(pfp)
            lum_img_arr =np.array(lum_img)
            final_img_arr = np.dstack((img_arr,lum_img_arr))
            circle_pfp_fn = f"{self.reactions_dir}/circle_pfp.png"
            Image.fromarray(final_img_arr).save(circle_pfp_fn) # DELETE THIS FILE AT THE END


            # create composite image with pfp template and circle pfp
            circle_pfp = Image.open(circle_pfp_fn)

            user_status = user.raw_status # get user status as a string (online, dnd, idle, offline)
            pfp_template_fn = f"{self.reactions_dir}/pfp_template_{user_status}"
            pfp_template = Image.open(pfp_template_fn)

            circle_pfp.paste(pfp_template)

            img.paste(circle_pfp, (420, 250))

            os.remove(pfp_filename)
            os.remove(circle_pfp_fn)

        else:
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
                start_x = round(start_box[0] + (dist_to_bonked_head * 1/len(text)))
                start_box = (start_x, start_box[1])
            
            I1.text(start_box, text, font=font, stroke_width=2, fill="black")

        # save new image with text
        img.save(img_filename)

        # open and send new image
        with open(img_filename, "rb") as bonk_img:
            bonk = discord.File(bonk_img)
        
        await ctx.send(file=bonk)

        # delete new image
        os.remove(img_filename)

    # sends an image of the profile picture of the tagged member
    # if no one is tagged, the pfp of the person that used the command is sent
    @commands.command()
    async def pfp(self, ctx: commands.context.Context):
        # check the mentions
        # if no mentions then send the pfp of the command user
        mentions = ctx.message.mentions
        
        if not mentions:
            user = ctx.author
            await ctx.send(user.avatar_url)

            return
        else:
            # if there are multiple mentions, only the pfp of the first is sent
            await ctx.send(mentions[0].avatar_url)

    # sends an image of the colour specified
    @commands.command()
    async def colour(self, ctx, *colour):
        lower_colour = [word.lower() for word in colour]
        
        colour = "".join(lower_colour)
        img = Image.new("P", (100, 100), None)
        im = ImageDraw.Draw(img)
        im.rectangle((0, 0, 100, 100), colour)

        img.save(f"{colour}.png")

        with open(f"{colour}.png", "rb") as colour_pic:
            pic = discord.File(colour_pic)

        await ctx.send(file=pic)

        os.remove(f"{colour}.png")

def setup(bot: commands.Bot):
    bot.add_cog(Reactions(bot))