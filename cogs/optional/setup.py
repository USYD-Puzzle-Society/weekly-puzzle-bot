import os
import json
import discord
import datetime
from typing import Callable
from discord.ext import commands


class Setup(commands.GroupCog, group_name="set"):
    def __init__(self, bot: commands.Bot, info):
        self.bot = bot
        self.info = info
        self.datetime_format = "%d/%m/%Y %H:%M"

    def new_time_and_week(self, puzzle):
        new_datetime = datetime.datetime.strptime(puzzle.release_time, self.datetime_format)
        new_datetime = new_datetime + datetime.timedelta(days=7)
        new_datetime = new_datetime.strftime(self.datetime_format)

        return (new_datetime, puzzle.week + 1)

    async def get_image_urls(self, interaction: discord.Interaction, message_from_user: Callable):
        await interaction.channel.send(
            "Please send all the images for the puzzle in one message."
            + " Type `.stop` at any time and no changes will be made."
        )

        msg = await self.bot.wait_for("message", check=message_from_user)

        if ".stop" == msg.content.lower():
            await interaction.channel.send("Command stopped. No changes have been made.")
            return []

        while not len(msg.attachments):
            await interaction.channel.send(
                "Please send all the images for the puzzle in one message."
                + " Type `.stop` at any time and no changes will be made."
            )

            msg = await self.bot.wait_for("message", check=message_from_user)

            if ".stop" == msg.content.lower():
                await interaction.channel.send("Command stopped. No changes have been made.")
                return []

        return [image.url for image in msg.attachments]

    @discord.app_commands.command(
        name="puzzle"
    )
    @commands.has_role("Executives")
    async def set_puzzle(
            self, interaction: discord.Interaction, puzzle_name: str, 
            submission_link: str, interactive_link: str = "",
            change_time: bool = True):
        puzzle_name = await self.info.check_puzzle_name(interaction, puzzle_name)
        if not puzzle_name:
            return

        await interaction.response.send_message(
            f"Puzzle setup started. The puzzle that you are setting has a {puzzle_name} puzzle classification."
        )

        puzzle = self.info.puzzles[puzzle_name]

        if change_time:
            release_time, week = self.new_time_and_week(puzzle)
        else:
            release_time = puzzle.release_time
            week_num = puzzle.week

        def message_from_user(msg):
            return msg.author == interaction.user

        img_urls = await self.get_image_urls(interaction, message_from_user)
        if img_urls == []:
            return
        
        puzzle.release_time = release_time
        puzzle.week = week
        puzzle.image_urls = img_urls
        puzzle.submission_link = submission_link
        puzzle.interactive_link = interactive_link

        self.info.save()
        text = puzzle.get_text(interaction, False)
        
        await interaction.channel.send(
            f"Done. The following will be released at {puzzle.release_time} in "
            + f"<#{puzzle.release_channel}>. "
            + f"Remember to do `.start {puzzle_name}`"
        )
        await interaction.channel.send(text)
        for i in range(len(img_urls)):
            await interaction.channel.send(img_urls[i])

    @discord.app_commands.command(
        name="release"
    )
    @commands.has_role("Executives")
    async def set_time(
            self, interaction: discord.Interaction, puzzle_name: str, date: str, 
            time: str): 
        puzzle_name = await self.info.check_puzzle_name(interaction, puzzle_name)
        if not puzzle_name:
            return

        new_time = await self.info.check_time(interaction, " ".join((date, time)))
        if not new_time:
            return

        puzzle = self.info.puzzles[puzzle_name]

        await interaction.response.send_message(
            "The previous release date for the puzzle was "
            + f"{puzzle.release_time}. "
            + "The new release time for the puzzle is "
            + f"{new_time}. "
            + f"Remember to do `.start {puzzle_name}`"
        )

        puzzle.release_time = new_time
        self.info.save()

    @discord.app_commands.command(
        name="week"
    )
    @commands.has_role("Executives")
    async def set_week(
            self, interaction: discord.Interaction, puzzle_name: str,
            week: int):
        puzzle_name = await self.info_obj.check_puzzle_name(interaction, puzzle_name)
        if not puzzle_name:
            return

        puzzle = self.info.puzzles[puzzle_name]
        
        await interaction.response.send_message(
            "The previous week number for the puzzle was "
            + f"{puzzle.week}. "
            + "The new week number for the puzzle is "
            + f"{week}. "
            + f"Remember to do `.start {puzzle_name}`"
        )

        puzzle.week = week
        self.info.save()


async def setup(bot: commands.Bot):
    info = bot.get_cog("Info")
    await bot.add_cog(Setup(bot, info), guild=discord.Object(1153319575048437833))