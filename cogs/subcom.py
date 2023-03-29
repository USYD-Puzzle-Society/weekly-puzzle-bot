import discord
from discord.ext import commands
import asyncio

exec_role = "Executives"
subcom_role = "Subcommittee"

class SubcomTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tasks = []

        '''
        self.tasks is a list of dictionaries
        Ideal format is going to be:
        [
            {
                "Task Name": "Testing 1 2 3",
                "Owner": None,
                "Due Date": None
            },
            {
                "Task Name": "Testing 4 5 6",
                "Owner": "turtle#6635",
                "Due Date": None
            }
        ]
        '''

    @commands.command()
    @commands.has_any_role(exec_role, subcom_role)
    async def tasks(self, ctx: commands.context.Context):
        embed_msg = discord.Embed(title="Active Tasks", color=discord.Color.greyple())
        
        # Pull tasks from storage
        # self.tasks = idk open memory and get stuff
        
        # Extract tasks
        temp_names = [task["Task Name"] for task in self.tasks]
        temp_owners = [task["Owner"] for task in self.tasks]
        temp_due_dates = [task["Due Date"] for task in self.tasks]
        embed_msg.add_field(name="Task Name", value="\n".join(temp_names), inline=True)
        embed_msg.add_field(name="Owner", value="\n".join(temp_owners), inline=True)
        embed_msg.add_field(name="Due Date", value="\n".join(temp_due_dates), inline=True)

        await ctx.send(embed=embed_msg)
        
    @commands.command(aliases=["addtask"])
    @commands.has_role(exec_role)
    async def add_task(self, ctx: commands.context.Context, *args):
        if not args:
            await ctx.send("Please use the command in the form `.addtask [Title of Task] [Due Date]`")
            return
        
        title = args[0]
        date = "None" if len(args) == 1 else args[1]
        new_task = {
            "Task Name": title,
            "Owner": ctx.author.mention,
            "Due Date": date
        }

        self.tasks.append(new_task)
    
    @commands.command()
    @commands.has_role(exec_role)
    async def assign_task(self, ctx: commands.context.Context, *args):
        user_roles = ctx.author.roles
        allowed_user = (self.exec_role in [role.name for role in user_roles]) #or "Subcommittee" in user_roles)

        if allowed_user:
            # If no argument, assign to author
            return True
        return False
    
    @commands.command()
    @commands.has_role(exec_role)
    async def remove_task(self, ctx: commands.context.Context, n: int):
        user_roles = ctx.author.roles
        allowed_user = (self.exec_role in [role.name for role in user_roles]) #or "Subcommittee" in user_roles)

        if allowed_user:
            # Check that n is a valid key in self.tasks
            return True
        # Reminder to log exited task into #archived-tasks w/ owner
        # and date of completion
        return False

def setup(bot: commands.Bot):
    bot.add_cog(SubcomTasks(bot))