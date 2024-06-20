from typing import Callable
import discord
from discord.ext import commands


class Setup(commands.GroupCog, group_name="set"):
    def __init__(self, bot: commands.Bot, puzzle_scheduler, info):
        self.bot = bot
        self.puzzle_scheduler = puzzle_scheduler
        self.info = info
        self.datetime_format = "%d/%m/%Y %H:%M"

    async def get_image_urls(self, interaction: discord.Interaction, message_from_user: Callable):
        await interaction.channel.send(
            "Please send all the images for the puzzle in one message."
            + " Type `exit` at any time to stop."
        )

        msg = await self.bot.wait_for("message", check=message_from_user)

        if "exit" == msg.content.lower():
            await interaction.channel.send("Command stopped. No changes have been made.")
            return []

        while not len(msg.attachments):
            await interaction.channel.send(
                "Please send all the images for the puzzle in one message."
                + " Type `exit` at any time to stop."
            )

            msg = await self.bot.wait_for("message", check=message_from_user)

            if "exit" == msg.content.lower():
                await interaction.channel.send("Command stopped. No changes have been made.")
                return []

        return [image.url for image in msg.attachments]

    @discord.app_commands.command(
        name="puzzle"
    )
    @commands.has_role("Executives")
    async def set_puzzle(
            self, interaction: discord.Interaction, puzzle_name: str, 
            submission_link: str, interactive_link: str = ""):
        puzzle_name = await self.info.check_puzzle_name(interaction, puzzle_name)
        if not puzzle_name:
            return

        await interaction.response.send_message(
            f"Puzzle setup started. The puzzle that you are setting has a {puzzle_name} puzzle classification."
        )

        puzzle = self.info.puzzles[puzzle_name]

        def message_from_user(msg):
            return msg.author == interaction.user

        image_urls = await self.get_image_urls(interaction, message_from_user)
        if image_urls == []:
            return
        
        puzzle.image_urls = image_urls
        puzzle.submission_link = submission_link
        puzzle.interactive_link = interactive_link
        self.info.save()

        text = puzzle.get_text(interaction.guild, False)
        
        await interaction.channel.send(
            f"Done. The following will be released at {puzzle.release_time} in "
            + f"<#{puzzle.release_channel}>."
            + f"<#{puzzle.release_channel}>. It will mention the role `{role_name}`."
        )
        await interaction.channel.send(text)
        for i in range(len(image_urls)):
            await interaction.channel.send(image_urls[i])

    @discord.app_commands.command(
        name="channel"
    )
    async def set_channel(
            self, interaction: discord.Interaction, puzzle_name: str, 
            channel_id: str):
        puzzle_name = await self.info.check_puzzle_name(interaction, puzzle_name)
        if not puzzle_name:
            return

        puzzle = self.info.puzzles[puzzle_name]

        await interaction.response.send_message(
            "The previous release channel for the puzzle was "
            + f"<#{puzzle.release_channel}>. "
            + "The new release channel for the puzzle is "
            + f"<#{channel_id}>."
        )

        puzzle.release_channel = int(channel_id)
        self.info.save()

    @discord.app_commands.command(
        name="time"
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
            "The previous release time for the puzzle was "
            + f"{puzzle.release_time}. "
            + "The new release time for the puzzle is "
            + f"{new_time}."
        )

        puzzle.release_time = new_time
        self.info.save()
        self.puzzle_scheduler.reschedule_puzzle(puzzle_name)

    @discord.app_commands.command(
        name="week"
    )
    @commands.has_role("Executives")
    async def set_week(
            self, interaction: discord.Interaction, puzzle_name: str,
            week: int):
        puzzle_name = await self.info.check_puzzle_name(interaction, puzzle_name)
        if not puzzle_name:
            return

        puzzle = self.info.puzzles[puzzle_name]
        
        await interaction.response.send_message(
            "The previous week number for the puzzle was "
            + f"{puzzle.week}. "
            + "The new week number for the puzzle is "
            + f"{week}."
        )

        puzzle.week = week
        self.info.save()


async def setup(bot: commands.Bot):
    puzzle_scheduler = bot.get_cog("PuzzleScheduler")
    info = bot.get_cog("Info")
    await bot.add_cog(Setup(bot, puzzle_scheduler, info), guild=discord.Object(1153319575048437833))