import json
import os
import datetime
import discord
from discord.ext import commands

class Set(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.info_fn = "info.json" # fn = filename
        self.datetime_format = "%Y-%m-%dT%H:%M"

        if os.path.exists(self.info_fn):
            self.info = json.loads(self.info_fn)
        else:
            self.info = {
                "puzzles": {
                    "datetime": "",
                    "week_num": -1,
                    "img_urls": [],
                    "speed_bonus": -1,
                    "submission_link": ""
                },
                "sb": {
                    "datetime": "",
                    "week_num": -1,
                    "img_url": "",
                    "submission_link": ""
                },
                "ciyk": {
                    "datetime": "",
                    "week_num": -1,
                    "img_url": "",
                    "submission_link": ""
                }
            }

    def format_date(self, date: datetime.datetime) -> str:
        return date.strftime(self.datetime_format)

    # this method exists as just an easy way to change the puzzles data in one method call in setpuzzles    
    def change_puzz_data(self, new_data: dict):
        self.info["puzzles"]["week_num"] = new_data["week_num"]
        self.info["puzzles"]["img_urls"] = new_data["urls"]
        self.info["puzzles"]["speed_bonus"] = new_data["speed_bonus"]
        self.info["puzzles"]["submission_link"] = new_data["submission_link"]

        # write the new info to the json file
        with open(self.info_fn, "w") as info:
            new_json = json.dumps(self.info, indent=4)

            info.write(new_json)

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
            await ctx.send("Command sotpped. No changes have been made to the puzzle info.")
            return
        else:
            new_data["submission_link"] = msg.content

        
        # if this point is reached, then the new data will be saved
        self.change_puzz_data(new_data)

    