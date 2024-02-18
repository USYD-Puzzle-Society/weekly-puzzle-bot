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
        self.info_obj = info
        self.datetime_format = "%d/%m/%Y %H:%M"

    # command for quick setup of puzzles. user will only have to send the images
    @commands.command()
    @commands.has_role("Executives")
    async def qset(self, ctx: commands.context.Context, preset: str, change_datetime: str):
        user = ctx.author

        def check(m):
            return m.author == user

        preset, accepted = self.info_obj.check_preset(preset)
        if not accepted:
            await ctx.send(f"Please use one of the accepted presets: {', '.join(self.info_obj.default_presets)}")
            return
        
        original_data = self.info_obj.info[preset]
        puzzle_data = {
            "release_datetime": original_data["release_datetime"],
            "week_num": original_data["week_num"],
            "img_urls": [],
            "submission_link": "",
            "interactive_link": ""
        }

        # change the date to be a week ahead of the previously stored date unless change_datetime is false
        if change_datetime.lower() not in ["false", "f"]:
            release_datetime = self.info_obj.str_to_datetime(puzzle_data["release_datetime"])
            release_datetime = release_datetime + datetime.timedelta(days=7)
            puzzle_data["release_datetime"] = release_datetime.strftime(self.datetime_format)

            # increase the week number to be one higher than the previously stored week
            puzzle_data["week_num"] = puzzle_data["week_num"] + 1

        # ask for images
        await ctx.send(
            "Please send all images for the puzzle in one message." + 
            " Type `.stop` at any time and no changes will be made."
        )

        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made.")
                return
            elif len(msg.attachments):
                puzzle_data["img_urls"] = [image.url for image in msg.attachments]
                break
            else:
                await ctx.send("Please send the images in one message.")
        
        # ask for submission link
        await ctx.send("Please send the submission link.")
        msg = await self.bot.wait_for("message", check=check)
        
        if ".stop" == msg.content.lower():
            await ctx.send("Command stopped. No changes have been made.")
            return
        else:
            puzzle_data["submission_link"] = msg.content
        
        # check for interactive link and ask for one if there is
        await ctx.send("Is there an interactive link? y/n")

        confirmation = False
        while not confirmation:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made.")
                return
            elif "y" == msg.content.lower():
                confirmation = "y"
            elif "n" == msg.content.lower():
                confirmation = "n"

        if "y" == confirmation:
            await ctx.send("Please send the interactive link for the puzzle.")

            link = await self.bot.wait_for("message", check=check)

            puzzle_data["interactive_link"] = link.content

        self.info_obj.change_data(preset, puzzle_data)

        # show the user the new changes
        text = self.info_obj.get_qtext(ctx, False, preset, original_data["week_num"])
        images = original_data["img_urls"]
        await ctx.send(f"Done. The following will be released at {original_data['release_datetime']} in <#{original_data['channel_id']}>. " +
        f"Remember to do `.start {preset}`")
        await ctx.send(text)
        for i in range(len(images)):
            await ctx.send(images[i])

    @commands.command()
    @commands.has_role("Executives")
    async def qsettime(self, ctx: commands.context.Context, preset: str, date: str, time: str):
        preset, accepted = self.info_obj.check_preset(preset)
        if not accepted:
            await ctx.send(f"Please use one of the accepted presets: {', '.join(self.info_obj.default_presets)}")
            return

        new_date = self.info_obj.check_is_date(date)
        if not new_date:
            await ctx.send("Please enter date in the format DD/MM/YYYY")
            return
        else:
            day, month, year = new_date

        release_date = datetime.date(year, month, day)
        weekday_name = self.info_obj.day_names[release_date.weekday()]

        new_time = self.info_obj.check_is_time(time)
        if not new_time:
            await ctx.send("Please enter time in the format HH:MM (24 hour time.)")
            return
        else:
            hour, minute = new_time

        new_release = datetime.datetime(year, month, day, hour, minute)
        self.info_obj.change_time(preset, new_release)
        await ctx.send(
            f"The new release time for the puzzles is {new_release.strftime(self.info_obj.datetime_format)} ({weekday_name}). " +
            f"Remember to do `.start {preset}`"
        )

    @commands.command()
    @commands.has_role("Executives")
    async def qsetweek(self, ctx: commands.context.Context, preset: str, week_num: str):
        preset, accepted = self.check_reset(preset)
        if not accepted:
            await ctx.send(f"Please use one of the accepted presets: {', '.join(self.default_presets)}")
            return

        new_week = 1
        try:
            new_week = int(week_num)
        except ValueError:
            await ctx.send("Please enter the week as a number.")
        
        self.info_obj.change_week(preset, new_week)
        await ctx.send(
            f"The new week number for the {preset.capitalize()} puzzle is {self.info_obj.info[preset]['week_num']}. " +
            f"Remember to do `.start {preset}`"
        )

    @commands.command()
    @commands.has_role("Executives")
    async def setrctime(self, ctx: commands.context.Context):
        user = ctx.author
        
        def check(m):
            return m.author == user
        
        await ctx.send(f"The current release time for the rebus and cryptic is {self.info_obj.info['rebuscryptic']['release_datetime']}")
        await ctx.send(
            "Please enter the new release date for the rebus and cryptic in the format DD/MM/YYYY." + 
            "Do `.stop` at any time to exit and no changes will be made to the release time of the rebus and cryptic."
        )

        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the release time of the rebus and cryptic.")
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
                await ctx.send("Command stopped. No changes have been made to the release time of the rebus and cryptic.")
                return
            
            time = self.info_obj.check_is_time(msg.content)
            if not time:
                await ctx.send("Please enter time in the format HH:MM (24 hour time.)")
            else:
                hour, minute = time
                break

        new_release = datetime.datetime(year, month, day, hour, minute)
        self.info_obj.change_time("rebuscryptic", new_release)
        await ctx.send(
            f"The new release time for the puzzles is {new_release.strftime(self.info_obj.datetime_format)} ({weekday_name}). " +
            "Remember to do `.start rc`"
        )

    """
    Thinking of making it so that this command allows the user to
    put the release date and time in the command call.
    Like: `.setminipuzztime 12/08/2022 11:00`
    """
    # commands to set the release time for the puzzles/ciyk
    @commands.command()
    @commands.has_role("Executives")
    async def setminipuzztime(self, ctx: commands.context.Context):
        user = ctx.author

        def check(m):
            return m.author == user

        # show current release time for puzzles
        await ctx.send(f'The current release time for the minipuzz is {self.info_obj.info["minipuzz"]["release_datetime"]}.')
        await ctx.send(
            "Please enter the new release date for the minipuzz in the format DD/MM/YYYY. " +
            "Do `.stop` at any time to exit and no changes will be made to the release time of the minipuzz."
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
                await ctx.send("Command stopped. No changes have been made to the release time of the puzzles.")
                return
            
            time = self.info_obj.check_is_time(msg.content)
            if not time:
                await ctx.send("Please enter time in the format HH:MM (24 hour time.)")
            else:
                hour, minute = time
                break
        
        new_release = datetime.datetime(year, month, day, hour, minute)
        self.info_obj.change_time("minipuzz", new_release)
        await ctx.send(
            f"The new release time for the puzzles is {new_release.strftime(self.info_obj.datetime_format)} ({weekday_name}). " +
            "Remember to do `.start minipuzz`"
        )

    @commands.command()
    @commands.has_role("Executives")
    async def setcrosswordtime(self, ctx: commands.context.Context):
        user = ctx.author

        def check(m):
            return m.author == user
        
        await ctx.send(f'The current release time for the crossword is {self.info_obj.info["crossword"]["release_datetime"]}.')
        await ctx.send(
            "Please enter the new release date for the crossword in the format DD/MM/YYYY. " +
            "Do `.stop` at any time to exit and no changes will be made to the release time of the crossword."
        )

        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the release time of the crossword.")
                return
            
            date = self.info_obj.check_is_date(msg.content)
            if not date:
                await ctx.send("Please enter the date in the format DD/MM/YYYY")
            else: 
                day, month, year = date
                break

        release_date = datetime.date(year, month, day)
        weekday_name = self.info_obj.day_names[release_date.weekday()]
        await ctx.send(f"The new release date is {release_date.strftime('%d/%m/%Y')} ({weekday_name})")
        await ctx.send(f"Please enter the new release time for the crossword in the format HH:MM (24 hour time)")

        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the release of the crossword.")
                return

            time = self.info_obj.check_is_time(msg.content)
            if not time:
                await ctx.send("Please enter time in the format HH:MM")
            else:
                hour, minute = time
                break

        new_release = datetime.datetime(year, month, day, hour, minute)
        self.info_obj.change_time("crossword", new_release)
        await ctx.send(
            f"The new release time for the crossword is {new_release.strftime(self.info_obj.datetime_format)} ({weekday_name}). " +
            "Remember to do `.start crossword`"
        )

    @commands.command()
    @commands.has_role("Executives")
    async def setwordsearchtime(self, ctx: commands.context.Context):
        user = ctx.author

        def check(m):
            return m.author == user
        
        await ctx.send(f'The current release time for the word search is {self.info_obj.info["wordsearch"]["release_datetime"]}.')
        await ctx.send(
            "Please enter the new release date for the sudoku in the format DD/MM/YYYY. " +
            "Do `.stop` at any time to exit and no changes will be made to the release time of the word search."
        )

        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the release time of the word search.")
                return
            
            date = self.info_obj.check_is_date(msg.content)
            if not date:
                await ctx.send("Please enter the date in the format DD/MM/YYYY")
            else: 
                day, month, year = date
                break

        release_date = datetime.date(year, month, day)
        weekday_name = self.info_obj.day_names[release_date.weekday()]
        await ctx.send(f"The new release date is {release_date.strftime('%d/%m/%Y')} ({weekday_name})")
        await ctx.send(f"Please enter the new release time for the logic puzzle in the format HH:MM (24 hour time)")

        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the release of the word search.")
                return

            time = self.info_obj.check_is_time(msg.content)
            if not time:
                await ctx.send("Please enter time in the format HH:MM")
            else:
                hour, minute = time
                break

        new_release = datetime.datetime(year, month, day, hour, minute)
        self.info_obj.change_time("wordsearch", new_release)
        await ctx.send(
            f"The new release time for the word search is {new_release.strftime(self.info_obj.datetime_format)} ({weekday_name}). " +
            "Remember to do `.start wordsearch`"
        )

    @commands.command()
    @commands.has_role("Executives")
    async def setlogicpuzztime(self, ctx: commands.context.Context):
        user = ctx.author

        def check(m):
            return m.author == user
        
        await ctx.send(f'The current release time for the logic puzzle is {self.info_obj.info["logicpuzz"]["release_datetime"]}.')
        await ctx.send(
            "Please enter the new release date for the sudoku in the format DD/MM/YYYY. " +
            "Do `.stop` at any time to exit and no changes will be made to the release time of the logic puzzle."
        )

        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the release time of the logic puzzle.")
                return
            
            date = self.info_obj.check_is_date(msg.content)
            if not date:
                await ctx.send("Please enter the date in the format DD/MM/YYYY")
            else: 
                day, month, year = date
                break

        release_date = datetime.date(year, month, day)
        weekday_name = self.info_obj.day_names[release_date.weekday()]
        await ctx.send(f"The new release date is {release_date.strftime('%d/%m/%Y')} ({weekday_name})")
        await ctx.send(f"Please enter the new release time for the logic puzzle in the format HH:MM (24 hour time)")

        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the release of the logic puzzle.")
                return

            time = self.info_obj.check_is_time(msg.content)
            if not time:
                await ctx.send("Please enter time in the format HH:MM")
            else:
                hour, minute = time
                break

        new_release = datetime.datetime(year, month, day, hour, minute)
        self.info_obj.change_time("logicpuzz", new_release)
        await ctx.send(
            f"The new release time for the logic puzzle is {new_release.strftime(self.info_obj.datetime_format)} ({weekday_name}). " +
            "Remember to do `.start logicpuzz`"
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

    # command to set info of rebuscryptic
    @commands.command()
    @commands.has_role("Executives")
    async def setrc(self, ctx: commands.context.Context):
        rc_info = self.info_obj.info["rebuscryptic"]
        user = ctx.author

        def check(m):
            return m.author == user
        
        await ctx.send(
            "Now setting the information for the rebus and cryptic." +
            "Type `.stop` at any time and no changes will be made to the current rebus and cryptic info."
        )
        await ctx.send("Please send the images for the rebus and cryptic in one message.")

        new_data = {
            "img_urls": [],
            "week_num": -1,
            "submission_link": "",
            "interactive_link": ""
        }

        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the rebus and cryptic.")
                return
            elif len(msg.attachments):
                new_data["img_urls"] = [image.url for image in msg.attachments]
                break
            else:
                await ctx.send("Please send the images for the minipuzz in one message.")

        await ctx.send("Please enter the week number.")

        is_number = False
        while not is_number:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the rebus and cryptic.")
                return
            
            try:
                week_num = int(msg.content)
                new_data["week_num"] = week_num

                is_number = True
            except ValueError:
                await ctx.send("Please enter a number.")

        # no check will be done to see if the link is a real link 
        await ctx.send("Please send the submission link for the rebus and cryptic.")
        msg = await self.bot.wait_for("message", check=check)
        
        if ".stop" == msg.content.lower():
            await ctx.send("Command stopped. No changes have been made to the minipuzz info.")
            return
        else:
            new_data["submission_link"] = msg.content

        # if this point is reached, then the new data will be saved
        self.info_obj.change_data("rebuscryptic", new_data)

        # show the user the new changes
        rc_text = self.info_obj.get_rebuscryptic_text(ctx, False)
        rc_images = rc_info["img_urls"]
        await ctx.send(f"Done. The following will be released at {rc_info['release_datetime']} in <#{rc_info['channel_id']}>" +
        "Remember to do `.start rc`")
        await ctx.send(rc_text)
        for i in range(len(rc_images)):
            await ctx.send(rc_images[i])

    # commands to set the announcement info for puzzles/ciyk
    @commands.command()
    @commands.has_role("Executives")
    async def setminipuzz(self, ctx: commands.context.Context):
        puzz_info = self.info_obj.info["minipuzz"]
        # get the user that is using the command
        user = ctx.author

        def check(m):
            return m.author == user
        
        await ctx.send(
            "Now setting the information for the minipuzz." +
            "Type `.stop` at any time and no changes will be made to the current minipuzz info."
        )
        # first ask for the images for the puzzles 
        await ctx.send("Please send the images for the minipuzz in one message.")

        new_data = {
            "img_urls": [],
            "week_num": -1,
            "submission_link": "",
            "interactive_link": ""
        }

        # enter loop that only breaks when user stops command or sends the puzzle images
        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the minipuzz info.")
                return
            elif len(msg.attachments):
                new_data["img_urls"] = [image.url for image in msg.attachments]
                break
            else:
                await ctx.send("Please send the images for the minipuzz in one message.")
        
        
        await ctx.send("Please enter the week number.")

        is_number = False
        while not is_number:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the minipuzz info.")
                return
            
            try:
                week_num = int(msg.content)
                new_data["week_num"] = week_num

                is_number = True
            except ValueError:
                await ctx.send("Please enter a number.")

        # no check will be done to see if the link is a real link 
        await ctx.send("Please send the submission link for the puzzles.")
        msg = await self.bot.wait_for("message", check=check)
        
        if ".stop" == msg.content.lower():
            await ctx.send("Command stopped. No changes have been made to the minipuzz info.")
            return
        else:
            new_data["submission_link"] = msg.content


        # add interactive link if there is one
        await ctx.send("Is there an interactive link? y/n")

        confirmation = False
        while not confirmation:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the minipuzz info.")
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
        self.info_obj.change_data("minipuzz", new_data)

        # show the user the new changes
        puzz_text = self.info_obj.get_minipuzz_text(ctx, False)
        puzz_images = puzz_info["img_urls"]
        await ctx.send(f'Done. The following will be released at {puzz_info["release_datetime"]} in <#{puzz_info["channel_id"]}>. ' +  
        'Remember to do `.start minipuzz`')
        await ctx.send(puzz_text)
        for i in range(len(puzz_images)):
            await ctx.send(puzz_images[i])
    
    @commands.command()
    @commands.has_role("Executives")
    async def setcrossword(self, ctx: commands.context.Context):
        crossword_info = self.info_obj.info["crossword"]
        user = ctx.author

        def check(m):
            return m.author == user
        
        await ctx.send("Now setting info for the crossword. Do `stop` at anytime and no changes will be made to the crossword.")

        new_data = {
            "img_urls": "",
            "week_num": -1,
            "submission_link": "",
            "interactive_link": ""
        }

        await ctx.send("Please send the images for the crossword.")

        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes will be made to the crossword.")
                return

            if len(msg.attachments):
                new_data["img_urls"] = [image.url for image in msg.attachments]
                break
            else:
                await ctx.send("Please send the image for the crossword.")

        # get week number
        await ctx.send("Please enter the week number.")
        is_number = False
        while not is_number:
            msg = await self.bot.wait_for("message", check=check)
            
            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes will be made to the crossword.")
                return

            try:
                new_week = int(msg.content)
                new_data["week_num"] = new_week
                is_number = True
            except ValueError:
                await ctx.send("Please enter a number.")

        # add interactive link if there is one
        await ctx.send("Is there an interactive link? y/n")

        confirmation = False
        while not confirmation:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the minipuzz info.")
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
        self.info_obj.change_data("crossword", new_data)

        # show the user the new changes
        crossword_text = self.info_obj.get_crossword_text(ctx, False)
        crossword_images = crossword_info["img_urls"]
        await ctx.send(
            f"Done. The following will be released at {crossword_info['release_datetime']} in <#{crossword_info['channel_id']}>. " + 
            "Remember to do `.start crossword`"
        )
        await ctx.send(crossword_text)
        for i in range(len(crossword_images)):
            await ctx.send(crossword_images[i])

    @commands.command()
    @commands.has_role("Executives")
    async def setwordsearch(self, ctx: commands.context.Context):
        wordsearch_info = self.info_obj.info["wordsearch"]
        user = ctx.author

        def check(m):
            return m.author == user
        
        await ctx.send("Now setting info for the word search. Do `.stop` at anytime and no changes will be made to the word search.")

        new_data = {
            "img_urls": "",
            "week_num": -1,
            "submission_link": "",
            "interactive_link": ""
        }

        await ctx.send("Please send the images for the word search.")

        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes will be made to the word search.")
                return
            
            if len(msg.attachments):
                new_data["img_urls"] = [image.url for image in msg.attachments]
                break
            else:
                await ctx.send("Please send the image for the logic puzzle.")

        # get week number
        await ctx.send("Please enter the week number.")
        is_number = False
        while not is_number:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes will be made to the logic puzzle.")
                return

            try:
                new_week = int(msg.content)
                new_data["week_num"] = new_week
                is_number = True
            except ValueError:
                await ctx.send("Please enter a number.")

        # if this point is reached, then the new data will be saved
        self.info_obj.change_data("wordsearch", new_data)

        # show the user the new changes
        wordsearch_text = self.info_obj.get_wordsearch_text(ctx, False)
        wordsearch_images = wordsearch_info["img_urls"]
        await ctx.send(
            f"Done. The following will be released at {wordsearch_info['release_datetime']} in <#{wordsearch_info['channel_id']}>. " + 
            "Remember to do `.start wordsearch`"
        )
        await ctx.send(wordsearch_text)
        for i in range(len(wordsearch_images)):
            await ctx.send(wordsearch_images[i])

    @commands.command()
    @commands.has_role("Executives")
    async def setlogicpuzz(self, ctx: commands.context.Context):
        logicpuzz_info = self.info_obj.info["logicpuzz"]
        user = ctx.author

        def check(m):
            return m.author == user
        
        await ctx.send("Now setting info for the logic puzzle. Do `.stop` at anytime and no changes will be made to the logic puzzle.")

        new_data = {
            "img_urls": "",
            "week_num": -1,
            "submission_link": "",
            "interactive_link": ""
        }

        await ctx.send("Please send the images for the logic puzzle.")

        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes will be made to the logic puzzle.")
                return

            if len(msg.attachments):
                new_data["img_urls"] = [image.url for image in msg.attachments]
                break
            else:
                await ctx.send("Please send the image for the logic puzzle.")

        # get week number
        await ctx.send("Please enter the week number.")
        is_number = False
        while not is_number:
            msg = await self.bot.wait_for("message", check=check)
            
            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes will be made to the logic puzzle.")
                return

            try:
                new_week = int(msg.content)
                new_data["week_num"] = new_week
                is_number = True
            except ValueError:
                await ctx.send("Please enter a number.")

        # add interactive link if there is one
        await ctx.send("Is there an interactive link? y/n")

        confirmation = False
        while not confirmation:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the minipuzz info.")
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
        self.info_obj.change_data("logicpuzz", new_data)

        # show the user the new changes
        logicpuzz_text = self.info_obj.get_logicpuzz_text(ctx, False)
        logicpuzz_images = logicpuzz_info["img_urls"]
        await ctx.send(
            f"Done. The following will be released at {logicpuzz_info['release_datetime']} in <#{logicpuzz_info['channel_id']}>. " + 
            "Remember to do `.start logicpuzz`"
        )
        await ctx.send(logicpuzz_text)
        for i in range(len(logicpuzz_images)):
            await ctx.send(logicpuzz_images[i])

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

async def setup(bot: commands.Bot):
    info = Info()
    await bot.add_cog(Setup(bot, info))