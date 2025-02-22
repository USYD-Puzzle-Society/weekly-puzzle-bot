import os
import json
import asyncio
import discord
import datetime
from discord import app_commands
from discord.ext import commands

from typing import Literal

EXEC_ROLE_NAME = "Executives"


class Start(commands.GroupCog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.info_fp = "info.json"
        self.start_fp = "start.json"

    # assumes given string format is %d/%m/%Y %H:%M
    def str_to_datetime(self, datetime_str: str) -> datetime.datetime:
        date, time = datetime_str.split()

        day, month, year = date.split("/")
        hour, minute = time.split(":")

        return datetime.datetime(
            int(year), int(month), int(day), int(hour), int(minute)
        )

    @app_commands.command(
        name="wpc", description="Start the release for the respective WPC puzzle."
    )
    @commands.has_role(EXEC_ROLE_NAME)
    async def start_wpc(
        self,
        interaction: discord.Interaction,
        release_day: Literal["Wednesday", "Friday"],
    ):
        await interaction.response.defer()

        # get the info from info.json
        if os.path.exists(self.info_fp):
            with open(self.info_fp, "r") as f:
                info = json.load(f)
        # error checking
        else:
            await interaction.followup.send(
                "No puzzles have been setup. Use `/setup wpc` to set the puzzles."
            )
            return

        try:
            puzz_data = info[f"{release_day}WPC"]
        except KeyError:
            await interaction.followup.send(
                "No puzzles have been setup. Use `/setup wpc` to set the puzzles."
            )
            return

        if puzz_data["releasing"]:
            await interaction.followup.send(
                f"The release for {release_day} has already been started."
            )
            return

        # get current time
        now = datetime.datetime.now()
        release_time = self.str_to_datetime(puzz_data["release_datetime"])
        release_id = str(now.microsecond)

        wait_time = (release_time - now).total_seconds()

        if wait_time < 0:
            await interaction.followup.send(
                "The current time is later than the release time. "
                + "Please change the release time before starting the release."
            )
            return

        if os.path.exists(self.start_fp):
            with open(self.start_fp, "r") as sj:
                currently_releasing = json.load(sj)
        else:
            currently_releasing = {}

        currently_releasing[release_id] = puzz_data
        with open(self.start_fp, "w") as sj:
            sj.write(json.dumps(currently_releasing, indent=4))

        # show user what will be released
        await interaction.followup.send(
            f"Starting! The following will be released at {puzz_data['release_datetime']} in <#{puzz_data['channel_id']}>. "
            + f"The ID for this release is {release_id}. Do `/stop {release_id}` to stop this release."
        )
        wpc_role = interaction.guild.get_role(puzz_data["role_id"])
        wpc_text = puzz_data["release_text"]
        await interaction.channel.send(f"@/{wpc_role}" + wpc_text)

        for img in puzz_data["img_urls"]:
            await interaction.channel.send(img)

        await asyncio.sleep(wait_time + 1)

        # check if release was stopped
        with open(self.start_fp, "r") as sj:
            currently_releasing = json.load(sj)

            if release_id not in currently_releasing:
                return

        # otherwise release the puzzles
        wpc_channel = interaction.guild.get_channel(puzz_data["channel_id"])
        await wpc_channel.send(f"{wpc_role.mention}" + wpc_text)
        for img in puzz_data["img_urls"]:
            await wpc_channel.send(img)

        del currently_releasing[release_id]
        new_json = json.dumps(currently_releasing, indent=4)
        with open(self.start_fp, "w") as sj:
            sj.write(new_json)

    @app_commands.command(
        name="jff", description="Start the release for the respective JFF puzzle."
    )
    @commands.has_role(EXEC_ROLE_NAME)
    async def start_jff(
        self,
        interaction: discord.Interaction,
        # release_day: str = Literal["Monday", "Friday"]
    ):
        await interaction.response.defer()

        release_day = "Monday"
        # get the info from info.json
        if os.path.exists(self.info_fp):
            with open(self.info_fp, "r") as f:
                info = json.load(f)
        # error checking
        else:
            await interaction.followup.send(
                "No puzzles have been setup. Use `/setup jff` to set the puzzles."
            )
            return

        try:
            puzz_data = info[f"{release_day}JFF"]
        except KeyError:
            await interaction.followup.send(
                "No puzzles have been setup. Use `/setup jff` to set the puzzles."
            )
            return

        if puzz_data["releasing"]:
            await interaction.followup.send(
                f"The release for {release_day} has already been started."
            )
            return

        # get current time
        now = datetime.datetime.now()
        release_time = self.str_to_datetime(puzz_data["release_datetime"])
        release_id = str(now.microsecond)

        wait_time = (release_time - now).total_seconds()

        if wait_time < 0:
            await interaction.followup.send(
                "The current time is later than the release time. "
                + "Please change the release time before starting the release."
            )
            return

        if os.path.exists(self.start_fp):
            with open(self.start_fp, "r") as sj:
                currently_releasing = json.load(sj)
        else:
            currently_releasing = {}

        currently_releasing[release_id] = puzz_data
        with open(self.start_fp, "w") as sj:
            sj.write(json.dumps(currently_releasing, indent=4))

        # show user what will be released
        await interaction.followup.send(
            f"Starting! The following will be released at {puzz_data['release_datetime']} in <#{puzz_data['channel_id']}>. "
            + f"The ID for this release is {release_id}. Do `/stop {release_id}` to stop this release."
        )
        jff_text = puzz_data["release_text"]
        await interaction.channel.send(jff_text)

        for img in puzz_data["img_urls"]:
            await interaction.channel.send(img)

        await asyncio.sleep(wait_time + 1)

        # check if release was stopped
        with open(self.start_fp, "r") as sj:
            currently_releasing = json.load(sj)

            if release_id not in currently_releasing:
                return

        # otherwise release the puzzles
        jff_channel = interaction.guild.get_channel(puzz_data["channel_id"])
        await jff_channel.send(jff_text)
        for img in puzz_data["img_urls"]:
            await jff_channel.send(img)

        del currently_releasing[release_id]
        new_json = json.dumps(currently_releasing, indent=4)
        with open(self.start_fp, "w") as sj:
            sj.write(new_json)


async def setup(bot: commands.Bot):
    await bot.add_cog(Start(bot))
