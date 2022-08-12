import json
import os
import datetime
import discord
from discord.ext import commands

class Set(commands.Cog):

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
                    "release_datetime": "08/08/2022 12:00",
                    "week_num": -1,
                    "img_urls": [],
                    "speed_bonus": -1,
                    "submission_link": ""
                },
                "sb": {
                    "role_name": "weekly games",
                    "release_datetime": "08/08/2022 12:00",
                    "week_num": -1,
                    "img_url": "",
                    "submission_link": ""
                },
                "ciyk": {
                    "role_name": "weekly games",
                    "release_datetime": "08/08/2022 12:00",
                    "week_num": -1,
                    "img_url": "",
                    "submission_link": ""
                }
            }
        
        self.puzz_datetime = self.str_to_datetime(self.info["puzzles"]["release_datetime"])
        self.sb_datetime = self.str_to_datetime(self.info["sb"]["release_datetime"])
        self.ciyk_datetime = self.str_to_datetime(self.info["ciyk"]["release_datetime"])

    def datetime_to_str(self, date: datetime.datetime) -> str:
        return date.strftime(self.datetime_format)

    # expects the %d/%m/%Y %H:%M format
    def str_to_datetime(self, string: str) -> datetime.datetime:
        date, time = string.split()

        day, month, year = date.split("/")
        hour, minute = time.split(":")

        return datetime.datetime(year, month, day, hour, minute)

    def get_puzz_text(self, ctx):
        role_name = self.info["puzzles"]["role_name"]
        puzz_tag = f"@/{discord.utils.get(ctx.guild.roles, name=role_name)}\n"
        line1 = f'{self.info["emojis"]["jigsaw"]} **WEEKLY PUZZLES: WEEK {self.info["puzzles"]["week_num"]}** {self.info["emojis"]["jigsaw"]}\n'
        line2 = f'**SPEED BONUS:** {self.info["puzzles"]["speed_bonus"]} MINUTES\n'
        line3 = f'*Hints will be unlimited after {self.info["puzzles"]["speed_bonus"]} minutes is up AND after the top 3 solvers have finished!*\n\n'
        line4 = f'**Submit your answers here:** {self.info["puzzles"]["submission_link"]}\n'
        line5 = "You can submit as many times as you want!\n"
        line6 = "Your highest score will be kept."

        return puzz_tag + line1 + line2 + line3 + line4 + line5 + line6

    # this method exists as just an easy way to change the puzzles data in one method call in setpuzzles    
    def change_puzz_data(self, new_data: dict[str]):
        self.info["puzzles"]["week_num"] = new_data["week_num"]
        self.info["puzzles"]["img_urls"] = new_data["urls"]
        self.info["puzzles"]["speed_bonus"] = new_data["speed_bonus"]
        self.info["puzzles"]["submission_link"] = new_data["submission_link"]

        # write the new info to the json file
        with open(self.info_fn, "w") as info:
            new_json = json.dumps(self.info, indent=4)

            info.write(new_json)

    """
    Thinking of making it so that this command allows the user to
    put the release date and time in the command call.
    Like: `.setpuzztime 12/08/2022 11:00`
    """
    @commands.command()
    async def setpuzztime(self, ctx):
        pass

    @commands.command()
    async def setpuzzles(self, ctx):
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
            "urls": [],
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
                new_data["urls"] = msg.attachments
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
        self.change_puzz_data(new_data)

        # show the user the new changes
        puzz_text = self.get_puzz_text(ctx)
        await ctx.send(f'Done. The following will be released at {self.info["puzzles"]["release_datetime"]}. Remember to do `.startpuzz`')
        await ctx.send(puzz_text)

    