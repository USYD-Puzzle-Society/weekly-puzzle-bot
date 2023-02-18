import os
import json
import discord
import datetime
from info import Info
from discord.ext import commands

class Setup(commands.Cog):

    def __init__(self, bot: commands.Bot, info: Info):
        self.bot = bot
        self.exec_id = "Executives"
        self.info_obj= info

    """
    Thinking of making it so that this command allows the user to
    put the release date and time in the command call.
    Like: `.setpuzztime 12/08/2022 11:00`
    """
    # commands to set the release time for the puzzles/ciyk
    @commands.command()
    @commands.has_role("Executives")
    async def setpuzztime(self, ctx: commands.context.Context):
        user = ctx.author

        def check(m):
            return m.author == user

        # show current release time for puzzles
        await ctx.send(f'The current release time for the puzzles is {self.info_obj.info["puzz"]["release_datetime"]}.')
        await ctx.send(
            "Please enter the new release date for the puzzles in the format DD/MM/YYYY. " +
            "Do `.stop` at any time to exit and no changes will be made to the release time of the puzzles."
        )

        # exit when valid date is given or .stop is typed
        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the release time of the puzzles.")
                return
            
            date = self.info_obj.check_is_date(msg.content)
            if not date:
                await ctx.send("Please enter date in the format DD/MM/YYYY")
            else:
                day, month, year = date
                break
        
        release_date = datetime.date(year, month, day)
        weekday_name = self.info_obj.day_names[release_date.weekday()]
        await ctx.send(f"The new release date is now {release_date.strftime('%d/%m/%Y')} ({weekday_name})")
        await ctx.send(f"Please enter the new release time for the puzzles in the format HH:MM (24 hour time).")

        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been amde to the release time of the puzzles.")
                return
            
            time = self.info_obj.check_is_time(msg.content)
            if not time:
                await ctx.send("Please enter time in the format HH:MM (24 hour time.)")
            else:
                hour, minute = time
                break
        
        new_release = datetime.datetime(year, month, day, hour, minute)
        self.info_obj.change_time("puzz", new_release)
        await ctx.send(
            f"The new release time for the puzzles is {new_release.strftime(self.info_obj.datetime_format)} ({weekday_name}). " +
            "Remember to do `.start puzz`"
        )

    @commands.command()
    @commands.has_role("Executives")
    async def setciyktime(self, ctx: commands.context.Context):
        user = ctx.author

        def check(m):
            return m.author == user

        await ctx.send(f'The current release time for CIYK is {self.info_obj.info["ciyk"]["release_datetime"]}.')
        await ctx.send(
            "Please enter the new release date for CIYK in the format DD/MM/YYYY. " +
            "Do `.stop` at any time to exit and no changes will be made to the release time of CIYK."
        )

        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the release time of CIYK.")
                return
            
            date = self.info_obj.check_is_date(msg.content)
            if not date:
                await ctx.send("Please enter the date in the format DD/MM/YYYY")
            else:
                day, month, year = date
                break

        release_date = datetime.date(year, month, day)
        weekday_name = self.info_obj.day_names[release_date.weekday()]
        await ctx.send(f'The new release date is {release_date.strftime("%d/%m/%Y")} ({weekday_name})')
        await ctx.send(f"Please enter the new release time for CIYK in the format HH:MM (24 hour time)")

        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been amde to the release of CIYK.")
                return

            time = self.info_obj.check_is_time(msg.content)
            if not time:
                await ctx.send("Please enter time in the format HH:MM")
            else:
                hour, minute = time
                break

        new_release = datetime.datetime(year, month, day, hour, minute)
        self.info_obj.change_time("ciyk", new_release)
        await ctx.send(
            f"The new release time for CIYK is {new_release.strftime(self.info_obj.datetime_format)} ({weekday_name}). " +
            "Remember to do `.start ciyk`"
        )

    
    # commands to set the announcement info for puzzles/ciyk
    @commands.command()
    @commands.has_role("Executives")
    async def setpuzzles(self, ctx: commands.context.Context):
        puzz_info = self.info_obj.info["puzz"]
        # get the user that is using the command
        user = ctx.author

        def check(m):
            return m.author == user
        
        await ctx.send(
            "Now setting the information for the puzzles." +
            "Type `.stop` at any time and no changes will be made to the current puzzle info."
        )
        # first ask for the images for the puzzles 
        await ctx.send("Please send the images for the puzzles in one message.")

        new_data = {
            "img_urls": [],
            "week_num": -1,
            "speed_bonus": -1,
            "submission_link": "",
            "interactive_link": ""
        }

        # enter loop that only breaks when user stops command or sends the puzzle images
        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the puzzle info.")
                return
            elif len(msg.attachments):
                new_data["img_urls"] = [image.url for image in msg.attachments]
                break
            else:
                await ctx.send("Please send the images for the puzzles in one message.")
        
        
        await ctx.send("Please enter the week number.")

        is_number = False
        while not is_number:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the puzzle info.")
                return
            
            try:
                week_num = int(msg.content)
                new_data["week_num"] = week_num

                is_number = True
            except ValueError:
                await ctx.send("Please enter a number.")
        

        await ctx.send("Please enter the speed bonus.")

        is_number = False
        while not is_number:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the puzzle info.")
                return
            
            try:
                speed_bonus = int(msg.content)
                new_data["speed_bonus"] = speed_bonus

                is_number = True
            except ValueError:
                await ctx.send("Please enter a number.")


        # no check will be done to see if the link is a real link 
        await ctx.send("Please send the submission link for the puzzles.")
        msg = await self.bot.wait_for("message", check=check)
        
        if ".stop" == msg.content.lower():
            await ctx.send("Command stopped. No changes have been made to the puzzle info.")
            return
        else:
            new_data["submission_link"] = msg.content


        # add interactive link if there is one
        await ctx.send("Is there an interactive link? y/n")

        confirmation = False
        while not confirmation:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the puzzle info.")
                return
            elif "y" == msg.content.lower():
                confirmation = "y"
            elif "n" == msg.content.lower():
                confirmation = "n"

        if "y" == confirmation:
            await ctx.send("Please send the interactive link for the puzzle.")

            link = await self.bot.wait_for("message", check=check)

            new_data["interactive_link"] = link.content

        
        # if this point is reached, then the new data will be saved
        self.info_obj.change_data("puzz", new_data)

        # show the user the new changes
        puzz_text = self.info_obj.get_puzz_text(ctx, False)
        puzz_images = puzz_info["img_urls"]
        await ctx.send(f'Done. The following will be released at {puzz_info["release_datetime"]} in <#{puzz_info["channel_id"]}>. ' +  
        'Remember to do `.start puzz`')
        await ctx.send(puzz_text)
        for i in range(len(puzz_images)):
            await ctx.send(puzz_images[i])
    
    @commands.command()
    @commands.has_role("Executives")
    async def setciyk(self, ctx: commands.context.Context):
        ciyk_info = self.info_obj.info["ciyk"]
        user = ctx.author

        def check(m):
            return m.author == user

        await ctx.send("Now setting info for CIYK. Do `.stop` at any time and no changes will be made to the CIYK announcement.")
        
        new_data = {
            "img_url": "",
            "week_num": -1,
            "submission_link": ""
        }

        # get image for ciyk
        await ctx.send("Please send the image for CIYK.")

        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes will be made to the CIYK announcement.")
                return

            if len(msg.attachments):
                new_data["img_url"] = msg.attachments[0].url
                break
            else:
                await ctx.send("Please send the image for CIYK")

        # get week number
        await ctx.send("Please enter the week number.")
        is_number = False
        while not is_number:
            msg = await self.bot.wait_for("message", check=check)
            
            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes will be made to the CIYK announcement.")
                return

            try:
                new_week = int(msg.content)
                new_data["week_num"] = new_week
                is_number = True
            except ValueError:
                await ctx.send("Please enter a number.")

        # store new data
        self.info_obj.change_data("ciyk", new_data)

        ciyk_text = self.info_obj.get_ciyk_text(ctx, False)
        await ctx.send(
            f"Done. The following will be released at {ciyk_info['release_datetime']} in <#{ciyk_info['channel_id']}>" +
            "Remember to do `.start ciyk`"
        )
        await ctx.send(ciyk_text)

def setup(bot: commands.Bot):
    info = Info()
    bot.add_cog(Setup(bot, info))