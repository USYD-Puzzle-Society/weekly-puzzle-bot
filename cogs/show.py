import os
import json
import discord
import datetime
from info import Info
from discord.ext import commands

class Show(commands.GroupCog, group_name="show"):
    def __init__(self, bot: commands.Bot, info: Info):
        self.bot = bot
        self.info_obj = info

    @discord.app_commands.command(
        name="puzzle"
    )
    @commands.has_role("Executives")
    async def show(self, interaction: discord.Interaction, puzzle_name: str):
        puzzle_name = await self.info_obj.check_puzzle_name(interaction, puzzle_name)
        if not puzzle_name:
            return
    
        puzzle_info = self.info_obj.info[puzzle_name]
        text = self.info_obj.get_text(interaction, False, puzzle_name)

        await interaction.response.send_message(
            f"The following will be released at "
            + f"{puzzle_info["release_datetime"]} "
            + f"in <#{puzzle_info["channel_id"]}>."
        )
        await interaction.channel.send(text)
        for i in range(len(puzzle_info["img_urls"])):
            await interaction.channel.send(puzzle_info["img_urls"][i])

async def setup(bot: commands.Bot):
    info = Info()
    await bot.add_cog(Show(bot, info), guild=discord.Object(1153319575048437833))