import os
import json
import asyncio
import discord
import datetime
from info import Info
from discord.ext import commands

class Start(commands.Cog):
    def __init__(self, bot: commands.Bot, info: Info):
        self.bot = bot
        self.info_obj = info
        
        self.start_json = "start.json"

    """
    Terminology is a bit confusing but for just the scope of this command,
    'puzz' refers to all the types of puzzles. i.e puzzles, second best and ciyk
    """
    @commands.command()
    @commands.has_role("Executives")
    async def start(self, ctx: commands.context.Context, puzz_name: str):
        puzz_name = puzz_name.lower()

        # get the current time
        now = datetime.datetime.now()

        # the release id is used to identify this specific puzzle release
        # if the user wants to stop this release from happening, then the id is used
        release_id = puzz_name

        if "rc" == puzz_name:
                    puzz_name = "rebuscryptic"
                    
        # get the puzzle info
        text = self.info_obj.get_text(ctx, puzz_name, True)
        no_mention_text = self.info_obj.get_text(ctx, puzz_name, False)
        
        if "ciyk" != puzz_name:
            urls = self.info_obj.info[puzz_name]["img_urls"]

        str_release = self.info_obj.info[puzz_name]["release_datetime"]
        release_datetime = self.info_obj.str_to_datetime(str_release)
        channel_id = self.info_obj.info[puzz_name]["channel_id"]
        channel = self.bot.get_channel(channel_id)

        # get wait time
        wait_time = (release_datetime - now).total_seconds()

        if 0 > wait_time:
            await ctx.send(
                "The current time is later than the release time. " +
                "Please change the release time before starting the release."
            )
            return

        if os.path.exists(self.start_json):
            with open(self.start_json, "r") as sj:
                currently_releasing = json.load(sj)
        else:
            currently_releasing = {}
        
        if "ciyk" != puzz_name:
            currently_releasing[release_id] = {
                "text": text,
                "urls": urls,
                "datetime": str_release,
                "channel": channel_id
            }
        else:
            currently_releasing[release_id] = {
                "text": text,
                "datetime": str_release,
                "channel": channel_id
            }

        # add the release to the json file
        with open(self.start_json, "w") as sj:
            new_json = json.dumps(currently_releasing, indent=4)

            sj.write(new_json)

        await ctx.send(
            f"Starting! The following will be released at {str_release} in <#{channel_id}>. " +
            f"The ID for this release is {release_id}. Do `.stop {release_id}` to stop this release."
        )
        await ctx.send(no_mention_text)
        if "ciyk" != puzz_name:
            for i in range(len(urls)):
                await ctx.send(urls[i])

        # sleep until release time
        await asyncio.sleep(wait_time+1)

        # check if the release was stopped
        with open(self.start_json, "r") as sj:
            currently_releasing = json.load(sj)

        if release_id not in currently_releasing:
            return
        else:
            await channel.send(text)
            if "ciyk" != puzz_name:
                for i in range(len(urls)):
                    await channel.send(urls[i])

            # remove from the json file
            with open(self.start_json, "r") as sj:
                currently_releasing = json.load(sj)

            del currently_releasing[release_id]

            new_json = json.dumps(currently_releasing, indent=4)

            with open(self.start_json, "w") as sj:
                sj.write(new_json)

def setup(bot: commands.Bot):
    info = Info()
    bot.add_cog(Start(bot, info))