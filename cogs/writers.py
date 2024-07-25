import discord
from discord.ext import commands
from discord import app_commands


class Writers(commands.GroupCog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.writers = {
            1039852128342118450: "Albert",
            419463237394759683: "Jayden",
            528058352274636810: "Simon",
            200214169612582913: "Stefan",
            # 549152699589984256: "Maria"
        }
        self.writers_role = "Executives"
        self.emojis = {
            "writer": ":writing_hand",
            "tick": ":white_check_mark",
            "cross": ":x:",
        }

    @app_commands.command(
        name="puzzthread",
        description="Create a thread based on a puzzle after providing the link.",
    )
    async def puzzthread(
        self, interaction: discord.Interaction, puzzle_link: str, thread_title: str
    ):
        await interaction.response.defer(ephemeral=True)
        try:
            writer = self.writers[interaction.user.id]
        except KeyError:
            await interaction.followup.send("You are not a writer!")
            return

        puzz_thread = await interaction.channel.create_thread(
            name=thread_title,
            auto_archive_duration=10080,
        )

        thread_msg = f"Puzzle: <{puzzle_link}>\n\n"
        thread_msg += f"{writer}: {self.emojis["writer"]}\n"

        for w_id, w in sorted(list(self.writers.items()), key=lambda x: x[1]):
            if w_id == interaction.user.id:
                continue
            thread_msg += f"{w}: :x:\n"

        thread_msg += f"\n{discord.utils.get(interaction.guild.roles, name=self.writers_role).mention}"

        await puzz_thread.send(thread_msg)
        await interaction.followup.send("Thread created!")

    @app_commands.command(
        name="testsolve",
        description="Mark the puzzle in the thread as testsolved (by you!)",
    )
    async def testsolve(self, interaction: discord.Interaction, undo: bool = False):
        await interaction.response.defer(ephemeral=True)
        try:
            testsolver = self.writers[interaction.user.id]
        except KeyError:
            await interaction.followup.send("You are not a testsolver!")
            return

        msg = [
            m async for m in interaction.channel.history(limit=1, oldest_first=True)
        ][0]
        spl_msg = msg.content.split("\n")
        for i, line in enumerate(spl_msg):
            if testsolver in line:
                # check writer status
                # there should only be two words separated by a space in lines with testsolvers' names
                _, status = line.split()
                if status == self.emoji["writer"]:
                    await interaction.followup.send("You can't testsolve your own puzzle bro...")
                    return

                if undo:
                    spl_msg[i] = f"{testsolver}: {self.emojis["cross"]}"
                else:
                    spl_msg[i] = f"{testsolver}: {self.emojis["tick"]}"

        new_msg = "\n".join(spl_msg)
        await msg.edit(content=new_msg)
        await interaction.followup.send("Testsolve status marked!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Writers(bot))
