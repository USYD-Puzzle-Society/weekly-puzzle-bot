import discord
from discord.ext import commands
from discord import app_commands

import os
import json

from typing import Literal

EXEC_ROLE_NAME = "Executives"


class Show(commands.GroupCog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

        self.info_fp = "info.json"

    @app_commands.command(
        name="wpc",
        description="Shows the current stored info for the respective WPC puzzle.",
    )
    @commands.has_role(EXEC_ROLE_NAME)
    async def show_wpc(
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
                f"The following will be released at {puzz_data['release_datetime']} in <#{puzz_data['channel_id']}>:"
            )
        else:
            await interaction.followup.send(
                f"The following will be released in <#{puzz_data['channel_id']}>. "
                + f"The release time is set for {puzz_data['release_datetime']} but the release has not been started yet. "
                + f"Do `/start wpc {release_day}` to start the release."
            )
        await interaction.channel.send(
            f"@/{interaction.guild.get_role(puzz_data['role_id'])}"
            + puzz_data["release_text"]
        )

        for img in puzz_data["img_urls"]:
            await interaction.channel.send(img)

    @app_commands.command(
        name="jff",
        description="Shows the current stored info for the respective JFF puzzle.",
    )
    @commands.has_role(EXEC_ROLE_NAME)
    async def show_jff(
        self,
        interaction: discord.Interaction,
        # release_day: Literal["Monday", "Friday"],
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
                f"The following will be released at {puzz_data['release_datetime']} in <#{puzz_data['channel_id']}>:"
            )
        else:
            await interaction.followup.send(
                f"The following will be released in <#{puzz_data['channel_id']}>. "
                + f"The release time is set for {puzz_data['release_datetime']} but the release has not been started yet. "
                + f"Do `/start wpc {release_day}` to start the release."
            )
        await interaction.channel.send(puzz_data["release_text"])

        for img in puzz_data["img_urls"]:
            await interaction.channel.send(img)


async def setup(bot: commands.Bot):
    await bot.add_cog(Show(bot))
