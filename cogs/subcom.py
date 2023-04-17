import discord
from discord.ext import commands
import asyncio
from classes.Task import Task

exec_role = "Executives"
subcom_role = "Subcommittee"

class SubcomTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tasks: list[Task] = []

        '''
        self.tasks is a list of Tasks
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
    async def add_task(self, ctx: commands.context.Context, args: "list[str]", role):
        task = Task(args[0] if args else "None", [ctx.author.mention])
        self.tasks.append(task)
        await ctx.send(f"New Task created with Task ID {task.task_id}")

    async def view_task(self, ctx: commands.context.Context, args: "list[str]", role):
        if not args:
            await ctx.send("You must provide a Task ID for viewing!")
            return
        to_be_viewed = self.find_task(args[0])
        if to_be_viewed:
            embed = discord.Embed(title=f"Task Details for Task {to_be_viewed.task_id}", color=discord.Color.greyple())
            embed.add_field(name="Task ID", value=to_be_viewed.task_id, inline=False)
            embed.add_field(name="Task Name", value=to_be_viewed.task_name, inline=False)
            embed.add_field(name="Owner", value=to_be_viewed.owner, inline=False)
            embed.add_field(name="Due Date", value=to_be_viewed.due_date, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Task {args[0]} not found!")

    async def view_all_tasks(self, ctx: commands.context.Context, args: "list[str]", role):
        '''
        view_all_task ignore all args given to it
        '''

        embed = discord.Embed(title="All Active Tasks", color=discord.Color.greyple())
        values = list(map(list, zip(*[task.to_tuple() for task in self.tasks]))) # cursed
        if not values:
            values = ["0.", "nothing!", "empty", "much wow"]
        embed.add_field(name="Tasks", value="\n".join((['. '.join(x) for x in zip([str(x) for x in values[0]], values[1])])))
        embed.add_field(name="Owner", value="\n".join([", ".join(owners) for owners in values[2]]))
        embed.add_field(name="Due Date", value="\n".join(values[3]))

        await ctx.send(embed=embed)
    
    async def assign_task(self, ctx: commands.context.Context, args: "list[str]", role):
        '''
        if args is empty, assign task to self
        otherwise, take a list of mentions
        '''
        if not args:
            await ctx.send("You must provide a Task ID for assignment!")
            return
        task = self.find_task(args[0])
        if not task:
            await ctx.send(f"Task {args[0]} not found!")
            return
        mentions = args[1:]
        if not mentions:
            task.owners = [ctx.author.mention]
        else:
            task.owners = args[1:]
        await ctx.send(f"Task {task.task_id} assigned to {task.owners_to_str()}")
    
    async def delete_task(self, ctx: commands.context.Context, args: "list[str]", role):
        if not args:
            await ctx.send("You must provide a Task ID for deletion!")
            return
        to_be_deleted = self.find_task(args[0])
        if to_be_deleted:
            self.tasks.remove(to_be_deleted)
            await ctx.send(f"Task {to_be_deleted.task_id} successfully deleted.")
        else:
            await ctx.send(f"Task {args[0]} not found!")
    
    def find_task(self, task_id: int) -> Task:
        result = None 
        for task in self.tasks:
            if (str(task.task_id) == task_id):
                result  = task
        return result
    
    @commands.command()
    @commands.has_any_role(exec_role, subcom_role)
    async def task(self, ctx: commands.context.Context, *args):
        if len(args) < 2 or args[0] not in ["subcom", "exec"] or args[1] not in ["add", "view", "viewall", "assign", "delete"]:
            await ctx.send("Please use the command in the form `.task [subcom/exec] [add/view/viewall/assign/delete]`")
            return
        role = discord.utils.get(ctx.guild.roles, name=exec_role)
        if args[0] == "exec" and role not in ctx.author.roles():
            await ctx.send("You must be an executive to perform this action!")
            return
        
        if args[1] == "add":
            await self.add_task(ctx, list(args)[2:], args[0])
        elif args[1] == "view":
            await self.view_task(ctx, list(args)[2:], args[0])
        elif args[1] == "viewall":
            await self.view_all_tasks(ctx, list(args)[2:], args[0])
        elif args[1] == "assign":
            await self.assign_task(ctx, list(args)[2:], args[0])
        elif args[1] == "delete":
            await self.delete_task(ctx, list(args)[2:], args[0])
        else:
            pass

async def setup(bot: commands.Bot):
    await bot.add_cog(SubcomTasks(bot))