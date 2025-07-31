import discord
from discord.ext import commands
from discord import app_commands, Member

WRITERS_ROLE_ID = "Writer Warriors"
TEST_SOLVER_ROLE_ID = "Test Solvers"

GUILD_ID = 877860838344634429

def member_is_writer(member):
    for role in member.roles:
        if role.name == WRITERS_ROLE_ID:
            return True
    return False

class Writers(commands.GroupCog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.set_test_solvers()
        self.writers_role = "Writer Warriors"
        self.emojis = {
            "writer": ":writing_hand:",
            "tick": ":white_check_mark:",
            "cross": ":x:",
        }

    def set_test_solvers(self):
        self.test_solvers: dict[int, str] = {}
        server = self.bot.get_guild(GUILD_ID)
        assert server

        for member in server.members:
            member_is_solver = False
            for role in member.roles:
                if role.name == TEST_SOLVER_ROLE_ID:
                    member_is_solver = True

            if member_is_solver:
                if member.nick:
                    self.test_solvers[member.id] = member.nick
                elif member.global_name:
                    self.test_solvers[member.id] = member.global_name
                else:
                    self.test_solvers[member.id] = member.name
            

    @app_commands.command(
        name="puzzthread",
        description="Create a thread based on a puzzle after providing the link.",
    )
    @commands.has_role(WRITERS_ROLE_ID)
    async def puzzthread(
        self, interaction: discord.Interaction, puzzle_link: str, thread_title: str
    ):
        await interaction.response.defer(ephemeral=True)

        if not member_is_writer(interaction.user):
            await interaction.followup.send("You are not a writer!")
            return

        self.set_test_solvers()

        puzz_thread = await interaction.channel.create_thread(
            name=thread_title,
            auto_archive_duration=10080,
        )

        writer = interaction.user.name
        thread_msg = f"Puzzle: <{puzzle_link}>\n\n"
        thread_msg += f"{writer}: {self.emojis['writer']}\n"

        for w_id, w in sorted(list(self.test_solvers.items()), key=lambda x: x[1]):
            if w_id == interaction.user.id:
                continue
            thread_msg += f"{w}: :x:\n"

        thread_msg += f"\n{discord.utils.get(interaction.guild.roles, name=TEST_SOLVER_ROLE_ID).mention}"

        sent_msg = await puzz_thread.send(thread_msg)
        await sent_msg.pin()

        await interaction.followup.send("Thread created!")

    @app_commands.command(
        name="testsolve",
        description="Mark the puzzle in the thread as testsolved (by you!)",
    )
    @commands.has_role(TEST_SOLVER_ROLE_ID)
    async def testsolve(self, interaction: discord.Interaction, undo: bool = False):
        await interaction.response.defer(ephemeral=True)

        if interaction.channel.type != discord.ChannelType.private_thread:
            await interaction.followup.send(
                "Please use this command in a puzzle thread."
            )
            return

        self.set_test_solvers()

        try:
            testsolver = self.test_solvers[interaction.user.id]
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
                if status == self.emojis["writer"]:
                    await interaction.followup.send(
                        "You can't testsolve your own puzzle bro..."
                    )
                    return

                if undo:
                    spl_msg[i] = f"{testsolver}: {self.emojis['cross']}"
                else:
                    spl_msg[i] = f"{testsolver}: {self.emojis['tick']}"

        new_msg = "\n".join(spl_msg)
        try:
            await msg.edit(content=new_msg)
            await interaction.followup.send("Testsolve status marked!")
        except discord.errors.Forbidden:
            await interaction.followup.send(
                "Please use this command in a puzzle thread."
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Writers(bot))
