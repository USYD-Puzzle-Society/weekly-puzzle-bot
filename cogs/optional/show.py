import discord
from discord.ext import commands
from cogs.required.info import Info


class Show(commands.GroupCog, group_name="show"):
    def __init__(self, bot: commands.Bot, info: Info):
        self.bot = bot
        self.info = info

    @discord.app_commands.command(
        name="puzzle",
        description="Shows the release time, content, and images of the specified puzzle."
    )
    @commands.has_role("Executives")
    async def show_puzzle(self, interaction: discord.Interaction, puzzle_name: str):
        puzzle_name = await self.info.check_puzzle_name(interaction, puzzle_name)
        if not puzzle_name:
            return
    
        puzzle = self.info.puzzles[puzzle_name]
        text = puzzle.get_text(interaction.guild, False)

        await interaction.response.send_message(
            f"The following will be released at {puzzle.release_time} in "
            + f"<#{puzzle.release_channel}>. It will mention the role `{puzzle.role_name}`."
        )
        await interaction.channel.send(text)
        for i in range(len(puzzle.image_urls)):
            await interaction.channel.send(puzzle.image_urls[i])


async def setup(bot: commands.Bot):
    info = bot.get_cog("Info")
    await bot.add_cog(Show(bot, info), guild=discord.Object(1267016354012336138))