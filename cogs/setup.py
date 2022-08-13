import os
import json
import discord
import datetime
from discord.ext import commands

class Setup(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.info_fn = "info.json" # fn = filename
        self.datetime_format = "%d/%m/%Y %H:%M"

        if os.path.exists(self.info_fn):
            self.info = json.loads(self.info_fn)
        else:
            self.info = {
                "emojis": {
                    "jigsaw": ":jigsaw:",
                    "brain": ":brain:",
                    "speech": ":speech_balloon:",
                    "heart": ":heart:",
                    "cross": ":x:"
                },
                "puzzles": {
                    "role_name": "weekly puzzles",
                    "channel_id": 892032997220573204,
                    "release_datetime": "08/08/2022 12:00",
                    "week_num": -1,
                    "img_urls": [],
                    "speed_bonus": -1,
                    "submission_link": ""
                },
                "sb": {
                    "role_name": "weekly games",
                    "channel_id": 1001742058601590824,
                    "release_datetime": "08/08/2022 12:00",
                    "week_num": -1,
                    "img_url": "",
                    "submission_link": ""
                },
                "ciyk": {
                    "role_name": "weekly games",
                    "channel_id": 1001742058601590824,
                    "discuss_id": 1001742642427744326,
                    "release_datetime": "08/08/2022 12:00",
                    "week_num": -1,
                    "img_url": "",
                    "submission_link": ""
                }
            }
        
        self.puzz_datetime = self.str_to_datetime(self.info["puzzles"]["release_datetime"])
        self.sb_datetime = self.str_to_datetime(self.info["sb"]["release_datetime"])
        self.ciyk_datetime = self.str_to_datetime(self.info["ciyk"]["release_datetime"])

        self.day_names = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }

    # expects the %d/%m/%Y %H:%M format
    def str_to_datetime(self, string: str) -> datetime.datetime:
        date, time = string.split()

        day, month, year = date.split("/")
        hour, minute = time.split(":")

        return datetime.datetime(year, month, day, hour, minute)

    # check for valid date
    def check_is_date(self, msg: str) -> tuple[int, int, int]|bool:
        try:
            strday, strmonth, stryear = msg.content.split("/")

            # check if it is a valid date
            date = datetime.date(int(stryear), int(strmonth), int(strday))

            day, month, year = int(strday), int(strmonth), int(stryear)

            return day, month, year
        
        except ValueError:
            return False

    # check for valid time
    def check_is_time(self, msg: str) -> tuple[int, int]|bool:
        try:
            strhour, strminute = msg.content.split(":")

            # check if valid time
            time = datetime.time(int(strhour), int(strminute))

            hour, minute = int(strhour), int(strminute)

            return hour, minute

        except ValueError:
            return False


    def get_puzz_text(self, ctx: commands.context.Context) -> str:
        emojis = self.info["emojis"]
        puzz_info = self.info["puzzles"]
        role_name = puzz_info["role_name"]
        puzz_tag = f"@/{discord.utils.get(ctx.guild.roles, name=role_name)}\n"
        line1 = f'{emojis["jigsaw"]} **WEEKLY PUZZLES: WEEK {puzz_info["week_num"]}** {emojis["jigsaw"]}\n'
        line2 = f'**SPEED BONUS:** {puzz_info["speed_bonus"]} MINUTES\n'
        line3 = f'*Hints will be unlimited after {puzz_info["speed_bonus"]} minutes is up AND after the top 3 solvers have finished!*\n\n'
        line4 = f'**Submit your answers here:** {puzz_info["submission_link"]}\n'
        line5 = "You can submit as many times as you want!\n"
        line6 = "Your highest score will be kept."

        return puzz_tag + line1 + line2 + line3 + line4 + line5 + line6

    def get_sb_text(self, ctx: commands.context.Context) -> str:
        emojis = self.info["emojis"]
        sb_info = self.info["sb"]
        role_name = sb_info["role_name"]
        sb_tag = f"@/{discord.utils.get(ctx.guild.roles, name=role_name)}\n"
        line1 = f'{emojis["brain"]} **SECOND BEST: WEEK {sb_info["week_num"]}** {emojis["brain"]}\n\n'
        line2 = f"Try your best to guess what the second most popular answer will be!\n\n"
        line3 = f'**Submit your answers here:** {sb_info["submission_link"]}\n\n'

        return sb_tag + line1 + line2 + line3 + sb_info["img_url"]
    
    def get_ciyk_text(self, ctx: commands.context.Context) -> str:
        emojis = self.info["emojis"]
        ciyk_info = self.info["ciyk"]
        role_name = ciyk_info["role_name"]
        ciyk_tag = f"@/{discord.utils.get(ctx.guild.roles, name=role_name)}\n\n"
        line1 = f'{emojis["speech"]} **COMMENT IF YOU KNOW: WEEK {ciyk_info["week_num"]}** {emojis["speech"]}\n'
        line2 = f'If you think you know the pattern, comment an answer that follows it in <#{ciyk_info["discuss_id"]}>\n'
        line3 = f'We\'ll react with a {emojis["heart"]} if you\'re right and a {emojis["cross"]} if you\'re wrong!\n\n'

        return ciyk_tag + line1 + line2 + line3 + ciyk_info["img_url"]

    # this method exists as just an easy way to change the data in one method call in setpuzzles/setsb/setciyk    
    def change_data(self, puzz_name: str, new_data: dict[str]):
        self.info[puzz_name]["week_num"] = new_data["week_num"]
        self.info[puzz_name]["submission_link"] = new_data["submission_link"]

        if "puzzles" == puzz_name:
            self.info[puzz_name]["img_urls"] = new_data["img_urls"]
            self.info[puzz_name]["speed_bonus"] = new_data["speed_bonus"]
        else:
            self.info[puzz_name]["img_url"] = new_data["img_url"]

        # write the new info to the json file so that it is not lost if the bot shuts down
        with open(self.info_fn, "w") as info:
            new_json = json.dumps(self.info, indent=4)

            info.write(new_json)

    """
    Thinking of making it so that this command allows the user to
    put the release date and time in the command call.
    Like: `.setpuzztime 12/08/2022 11:00`
    """
    @commands.command()
    async def setpuzztime(self, ctx: commands.context.Context):
        user = ctx.author

        def check(m):
            return m.author == user

        # show current release time for puzzles
        await ctx.send(f'The current release time for the puzzles is {self.info["puzzles"]["release_datetime"]}.')
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
            
            date = self.check_is_date(msg.content)
            if not date:
                await ctx.send("Please enter date in the format DD/MM/YYYY")
            else:
                day, month, year = date
                break
        
        release_date = datetime.date(year, month, day)
        weekday_name = self.day_names[release_date.weekday()]
        await ctx.send(f"The new release date is now {release_date.strftime('%d/%m/%Y')} ({weekday_name})")
        await ctx.send(f"Please enter the new release time for the puzzles in the format HH:MM (24 hour time).")

        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been amde to the release time of the puzzles.")
                return
            
            time = self.check_is_time(msg.content)
            if not time:
                await ctx.send("Please enter time in the format HH:MM (24 hour time.)")
            else:
                hour, minute = time
                break
        
        new_release = datetime.datetime(year, month, day, hour, minute)
        self.info["puzzles"]["release_datetime"] = new_release.strftime(self.datetime_format)
        await ctx.send(
            f"The new release time for the puzzles is {new_release.strftime(self.datetime_format)} ({weekday_name}). " +
            "Remember to do `.startpuzz`"
        )

    @commands.command()
    async def setsbtime(self, ctx: commands.context.Context):
        user = ctx.author

        def check(m):
            return m.author == user

        await ctx.send(f'The current release time for Second Best is {self.info["sb"]["release_datetime"]}.')
        await ctx.send(
            "Please enter the new release date for Second Best in the format DD/MM/YYYY. " +
            "Do `.stop` at any time to exit and no changes will be made to the release time of Second Best."
        )

        while True:
            msg = self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the release time of Second Best.")
                return
            
            date = self.check_is_date(msg.content)
            if not date:
                await ctx.send("Please enter the date in the format DD/MM/YYYY")
            else:
                day, month, year = date
                break

        release_date = datetime.date(day, month, year)
        weekday_name = self.day_names[release_date.weekday()]
        await ctx.send(f'The new release date is {release_date.strftime("%d/%m/%Y")} ({weekday_name})')
        await ctx.send(f"Please enter the new release time for Second Best in the format HH:MM (24 hour time)")

        while True:
            msg = self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been amde to the release of Second Best.")
                return

            time = self.check_is_time(msg.content)
            if not time:
                await ctx.send("Please enter time in the format HH:MM")
            else:
                hour, minute = time
                break

        new_release = datetime.datetime(year, month, day, hour, minute)
        self.info["sb"]["release_datetime"] = new_release.strftime(self.datetime_format)
        await ctx.send(
            f"The new release time for Second Best is {new_release.strftime(self.datetime_format)} ({weekday_name}). " +
            "Remember to do `.startsb`"
        )

    @commands.command()
    async def setciyktime(self, ctx: commands.context.Context):
        user = ctx.author

        def check(m):
            return m.author == user

        await ctx.send(f'The current release time for CIYK is {self.info["ciyk"]["release_datetime"]}.')
        await ctx.send(
            "Please enter the new release date for CIYK in the format DD/MM/YYYY. " +
            "Do `.stop` at any time to exit and no changes will be made to the release time of CIYK."
        )

        while True:
            msg = self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the release time of CIYK.")
                return
            
            date = self.check_is_date(msg.content)
            if not date:
                await ctx.send("Please enter the date in the format DD/MM/YYYY")
            else:
                day, month, year = date
                break

        release_date = datetime.date(day, month, year)
        weekday_name = self.day_names[release_date.weekday()]
        await ctx.send(f'The new release date is {release_date.strftime("%d/%m/%Y")} ({weekday_name})')
        await ctx.send(f"Please enter the new release time for CIYK in the format HH:MM (24 hour time)")

        while True:
            msg = self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been amde to the release of CIYK.")
                return

            time = self.check_is_time(msg.content)
            if not time:
                await ctx.send("Please enter time in the format HH:MM")
            else:
                hour, minute = time
                break

        new_release = datetime.datetime(year, month, day, hour, minute)
        self.info["ciyk"]["release_datetime"] = new_release.strftime(self.datetime_format)
        await ctx.send(
            f"The new release time for CIYK is {new_release.strftime(self.datetime_format)} ({weekday_name}). " +
            "Remember to do `.startciyk`"
        )

    @commands.command()
    async def setpuzzles(self, ctx: commands.context.Context):
        puzz_info = self.info["puzzles"]
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
            "submission_link": ""
        }

        # enter loop that only breaks when user stops command or sends the puzzle images
        while True:
            msg = await self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made to the puzzle info.")
                return
            elif len(msg.attachments):
                new_data["img_urls"] = msg.attachments
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
        msg = self.bot.wait_for("message", check=check)
        
        if ".stop" == msg.content.lower():
            await ctx.send("Command stopped. No changes have been made to the puzzle info.")
            return
        else:
            new_data["submission_link"] = msg.content

        
        # if this point is reached, then the new data will be saved
        self.change_data("puzzles", new_data)

        # show the user the new changes
        puzz_text = self.get_puzz_text(ctx)
        puzz_images = puzz_info["img_urls"]
        await ctx.send(f'Done. The following will be released at {puzz_info["release_datetime"]} in <#{puzz_info["channel_id"]}>. ' +  
        'Remember to do `.startpuzz`')
        await ctx.send(puzz_text)
        for i in range(len(puzz_images)):
            await ctx.send(puzz_images[i])

    @commands.command()
    async def setsb(self, ctx: commands.context.Context):
        sb_info = self.info["sb"]
        user = ctx.author
        
        def check(m):
            return m.author == user

        await ctx.send(
            "Now setting the info for Second Best." +
            "Type `.stop` at any time to exit and no changes will be made to the Second Best announcement."
        )

        new_data = {
            "img_url": "",
            "week_num": -1,
            "submission_link": ""
        }

        await ctx.send("Please send the image for Second Best.")

        while True:
            msg = self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes will be made to the Second Best announcement.")
                return

            if len(msg.attachments):
                # assuming that the first attachment is the sb image
                # if not then rip
                new_data["img_url"] = msg.attachments[0]
                break
            else:
                await ctx.send("Please send the image for Second Best.")
        

        await ctx.send("Please enter the week number.")

        is_number = False
        while not is_number:
            msg = self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes will be made to the Second Best announcement.")
                return
            
            try:
                new_week = int(msg.content)
                new_data["week_num"] = new_week
                is_number = True
            except ValueError:
                await ctx.send("Please enter a number.")
        

        await ctx.send("Please send the submission link.")

        msg = self.bot.wait_for("messsage", check=check)

        if ".stop" == msg.content.lower():
            await ctx.send("Command stopped. No changes will be made to the Second Best announcement.")
            return
        else:
            new_data["submission_link"] = msg.content

        # store the new data
        self.change_data("sb", new_data)

        sb_text = self.get_sb_text(ctx)
        await ctx.send(
            f"Done. The following will be sent at {sb_info['release_datetime']} <#{sb_info['channel_id']}>. " +
            "Remember to do `.startsb`"
        )
        await ctx.send(sb_text)
    
    @commands.command()
    async def setciyk(self, ctx: commands.context.Context):
        ciyk_info = self.info["ciyk"]
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
            msg = self.bot.wait_for("message", check=check)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes will be made to the CIYK announcement.")
                return

            if len(msg.attachments):
                new_data["img_url"] = msg.attachments[0]
                break
            else:
                await ctx.send("Please send the image for CIYK")

        # get week number
        await ctx.send("Please enter the week number.")
        is_number = False
        while not is_number:
            msg = self.bot.wait_for("message", check=check)
            
            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes will be made to the CIYK announcement.")
                return

            try:
                new_week = int(msg.content)
                new_data["week_num"] = new_week
                is_number = True
            except ValueError:
                await ctx.send("Please enter a number.")

        # get submission link
        await ctx.send("Please send the submission link.")

        msg = self.bot.wait_for("message", check=check)
        
        if ".stop" == msg.content.lower():
            await ctx.send("Command stopped. No changes will be made to the CIYK announcement.")
            return
        else:
            new_data["submission_link"] = msg.content

        # store new data
        self.change_data("ciyk", new_data)

        ciyk_text = self.get_ciyk_text(ctx)
        await ctx.send(
            f"Done. The following will be released at {ciyk_info['release_datetime']} in <#{ciyk_info['channel_id']}>" +
            "Remember to do `.startciyk`"
        )
        await ctx.send(ciyk_text)