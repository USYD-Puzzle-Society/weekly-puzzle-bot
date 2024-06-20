import discord
from discord.ext import commands


class Setup(commands.GroupCog, group_name="set"):
    def __init__(self, bot: commands.Bot, puzzle_scheduler, info):
        self.bot = bot
        self.puzzle_scheduler = puzzle_scheduler
        self.info = info
        self.datetime_format = "%d/%m/%Y %H:%M"

    async def get_image_urls(self, interaction: discord.Interaction):
        def message_from_user(msg):
            return msg.author == interaction.user
        
        await interaction.response.send_message(
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
        name="role"
    )
    @commands.has_role("Executives")
    async def set_role(
            self, interaction: discord.Interaction, puzzle_name: str,
            role_name: str):
        puzzle_name = await self.info.check_puzzle_name(interaction, puzzle_name)
        if not puzzle_name:
            return
        
        puzzle = self.info.puzzles[puzzle_name]

        await interaction.response.send_message(
            "The previous role for the puzzle was "
            + f"`{puzzle.role_name}`. "
            + "The new role for the puzzle is "
            + f"`{role_name}`."
        )

        puzzle.role_name = role_name
        self.info.save()

    @discord.app_commands.command(
        name="channel"
    )
    @commands.has_role("Executives")
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
            self, interaction: discord.Interaction, puzzle_name: str, 
            date: str, time: str): 
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

    @discord.app_commands.command(
        name="images"
    )
    @commands.has_role("Executives")
    async def set_images(self, interaction: discord.Interaction, puzzle_name: str):
        puzzle_name = await self.info.check_puzzle_name(interaction, puzzle_name)
        if not puzzle_name:
            return

        puzzle = self.info.puzzles[puzzle_name]

        image_urls = await self.get_image_urls(interaction)
        if image_urls == []:
            return

        if len(image_urls) == 1:
            await interaction.channel.send(
                "The new image link for the puzzle is "
                + f"{image_urls[0]}."
            )
        else:
            await interaction.channel.send(
                "The new image links for the puzzle are "
                + f"{', '.join(image_urls)}."
            )

        puzzle.image_urls = image_urls
        self.info.save()

    @discord.app_commands.command(
        name="links"
    )
    @commands.has_role("Executives")
    async def set_links(
            self, interaction: discord.Interaction, puzzle_name: str, 
            submission_link: str, interactive_link: str = ""):
        puzzle_name = await self.info.check_puzzle_name(interaction, puzzle_name)
        if not puzzle_name:
            return

        puzzle = self.info.puzzles[puzzle_name]

        message = ("The previous submission link for the puzzle was "
            + f"{puzzle.submission_link}. "
            + "The new submission link for the puzzle is "
            + f"{submission_link}.")
        
        if interactive_link:
            message += ("\n\nThe previous interactive link for the puzzle was "
                + f"{puzzle.interactive_link}. "
                + "The new interactive link for the puzzle is "
                + f"{interactive_link}.")
        
        await interaction.response.send_message(message)

        puzzle.submission_link = submission_link
        puzzle.interactive_link = interactive_link
        self.info.save()


async def setup(bot: commands.Bot):
    puzzle_scheduler = bot.get_cog("PuzzleScheduler")
    info = bot.get_cog("Info")
    await bot.add_cog(Setup(bot, puzzle_scheduler, info), guild=discord.Object(1153319575048437833))