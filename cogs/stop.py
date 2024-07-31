import os
import json
import discord
from discord import app_commands
from discord.ext import commands

EXEC_ROLE_NAME = "Executives"


class Stop(commands.GroupCog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.start_fp = "start.json"

    @app_commands.command(
        name="release", description="Stop the release for the given WPC puzzle."
    )
    @commands.has_role(EXEC_ROLE_NAME)
    async def stop(self, interaction: discord.Interaction, release_id: int):
        await interaction.response.defer()

        # get the info from info.json
        if os.path.exists(self.start_fp):
            with open(self.start_fp, "r") as f:
                starting_puzzles = json.load(f)
        # error checking
        else:
            await interaction.followup.send(
                "No puzzles have been scheduled for release. Use `/start [wpc/jff]` to start a release."
            )
            return

        if str(release_id) not in starting_puzzles:
            await interaction.followup.send(
                f"A puzzle with the release ID {release_id} has not been scheduled."
            )
            return

        del starting_puzzles[str(release_id)]

        with open(self.start_fp, "w") as sj:
            sj.write(json.dumps(starting_puzzles, indent=4))

        await interaction.followup.send(
            f"Puzzle with release ID {release_id} has been stopped."
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Stop(bot))
