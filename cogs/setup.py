import os
import json
import discord
import datetime
from typing import Callable
from info import Info
from discord.ext import commands


class Setup(commands.Cog):
    def __init__(self, bot: commands.Bot, info: Info):
        self.bot = bot
        self.exec_id = "Executives"
        self.info_obj = info
        self.datetime_format = "%d/%m/%Y %H:%M"

    async def check_puzzle_name(self, interaction: discord.Interaction, puzzle_name: str):
        puzzle_name = self.info_obj.check_puzzle_name(puzzle_name)
        if not puzzle_name:
            accepted_puzzle_names = ', '.join(self.info_obj.default_puzzle_names)
            await interaction.channel.send(f"Please use one of the accepted puzzle_names: {accepted_puzzle_names}")
            return False

        return puzzle_name

    async def check_date(self, interaction: discord.Interaction, date: str):
        date = self.info_obj.check_date(date)
        if not date:
            await interaction.response.send_message("Please enter date in the format DD/MM/YYYY")
            return False

        return date

    async def check_time(self, interaction: discord.Interaction, time: str):
        time = self.info_obj.check_time(time)
        if not time:
            await interaction.response.send_message("Please enter time in the format HH:MM (24 hour time.)")
            return False
        
        return time

    def new_datetime_and_week(self, original_datetime: str, original_week: int):
        new_datetime = self.info_obj.str_to_datetime(original_datetime)
        new_datetime = new_datetime + datetime.timedelta(days=7)
        new_datetime = new_datetime.strftime(self.datetime_format)

        return (new_datetime, original_week + 1)

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

    async def get_submission_link(self, interaction: discord.Interaction, message_from_user: Callable):
        await interaction.channel.send("Please send the submission link.")

        msg = await self.bot.wait_for("message", check=message_from_user)

        if ".stop" == msg.content.lower():
            await interaction.channel.send("Command stopped. No changes have been made.")
            return ""

        return msg.content

    async def get_interactive_link(self, interaction: discord.Interaction, message_from_user: Callable):
        await interaction.channel.send("Is there an interactive link? y/n")

        msg = await self.bot.wait_for("message", check=message_from_user)

        if ".stop" == msg.content.lower():
            await interaction.channel.send("Command stopped. No changes have been made.")
            return ""

        while not msg.content.lower() == "y":
            if "n" == msg.content.lower():
                return ""

            await interaction.channel.send("Is there an interactive link? y/n")

            msg = await self.bot.wait_for("message", check=message_from_user)

            if ".stop" == msg.content.lower():
                await interaction.channel.send("Command stopped. No changes have been made.")
                return ""
            
        await interaction.channel.send("Please send the interactive link for the puzzle.")

        msg = await self.bot.wait_for("message", check=message_from_user)

        if ".stop" == msg.content.lower():
            await interaction.channel.send("Command stopped. No changes have been made.")
            return ""

        return msg.content

    # command for quick setup of a puzzle. user will only have to send the images
    @discord.app_commands.command(
        name="setpuzzle"
    )
    @commands.has_role("Executives")
    async def set_puzzle(
            self, interaction: discord.Interaction, puzzle_name: str, 
            change_datetime: bool = True):
        def message_from_user(msg):
            return msg.author == interaction.user

        await interaction.response.send_message(
            f"Puzzle setup started. The puzzle your are setting has a {puzzle_name} puzzle classification."
        )

        puzzle_name = await self.check_puzzle_name(interaction, puzzle_name)
        if not puzzle_name:
            return

        original_data = self.info_obj.info[puzzle_name]

        if change_datetime:
            release_datetime, week_num = self.new_datetime_and_week(
                original_data["release_datetime"], 
                original_data["week_num"]
            )
        else:
            release_datetime = original_data["release_datetime"]
            week_num = original_data["week_num"]

        img_urls = await self.get_image_urls(interaction, message_from_user)
        if img_urls == []:
            return

        submission_link = await self.get_submission_link(interaction, message_from_user)
        if submission_link == "":
            return

        interactive_link = await self.get_interactive_link(interaction, message_from_user)
        
        puzzle_data = {
            "release_datetime": release_datetime,
            "week_num": week_num,
            "img_urls": img_urls,
            "submission_link": submission_link,
            "interactive_link": interactive_link,
        }

        self.info_obj.change_data(puzzle_name, puzzle_data)
        
        await interaction.channel.send(
            f"Done. The following will be released at {release_datetime} in "
            + f"<#{original_data['channel_id']}>. "
            + f"Remember to do `.start {puzzle_name}`"
        )

        text = self.info_obj.get_text(interaction, False, puzzle_name)
        await interaction.channel.send(text)
        for i in range(len(img_urls)):
            await interaction.channel.send(img_urls[i])

    """
    Thinking of making it so that this command allows the user to
    put the release date and time in the command call.
    Like: `.setminipuzztime 12/08/2022 11:00`
    """

    @discord.app_commands.command(
        name="setrelease"
    )
    @commands.has_role("Executives")
    async def set_time(
            self, interaction: discord.Interaction, puzzle_name: str, date: str, 
            time: str): 
        puzzle_name = await self.check_puzzle_name(interaction, puzzle_name)
        if not puzzle_name:
            return

        previous_datetime = self.info_obj.info[puzzle_name]['release_datetime']

        new_date = await self.check_date(interaction, date)
        if not new_date:
            return
        day, month, year = new_date

        release_date = datetime.date(year, month, day)
        weekday_name = self.info_obj.day_names[release_date.weekday()]

        new_time = await self.check_time(interaction, time)
        if not new_time:
            return
        hour, minute = new_time

        new_release = datetime.datetime(year, month, day, hour, minute)
        self.info_obj.change_time(puzzle_name, new_release)

        await interaction.response.send_message(
            "The previous release date for the puzzle was "
            + f"{previous_datetime}. "
            + "The new release time for the puzzle is "
            + f"{self.info_obj.info[puzzle_name]['release_datetime']} ({weekday_name}). "
            + f"Remember to do `.start {puzzle_name}`"
        )

    @discord.app_commands.command(
        name="setweek"
    )
    @commands.has_role("Executives")
    async def set_week(
            self, interaction: discord.Interaction, puzzle_name: str,
            week_num: int):
        puzzle_name = await self.check_puzzle_name(interaction, puzzle_name)
        if not puzzle_name:
            return

        previous_week = self.info_obj.info[puzzle_name]['week_num']
        self.info_obj.change_week(puzzle_name, new_week)

        await interaction.response.send_message(
            "The previous week number for the puzzle was "
            + f"{previous_week}. "
            + "The new week number for the puzzle is "
            + f"{week_num}. "
            + f"Remember to do `.start {puzzle_name}`"
        )


async def setup(bot: commands.Bot):
    info = Info()
    await bot.add_cog(Setup(bot, info), guild=discord.Object(1153319575048437833))