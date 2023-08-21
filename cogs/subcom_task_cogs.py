import discord
from discord.ext import commands
import datetime

from classes.Task import Task
from classes.ArchivedTask import ArchivedTask
from src import subcom_task
from src.subcom_task_errors import TaskNotFoundError
from src.subcom_task_errors import IllegalTaskIDError
from embeds.subcom_task_embeds import task_view_embed, tasks_list_view_embed

exec_role = "Executives"
subcom_role = "Subcommittee"
archive_channel = None

class SubcomTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def new_task(self, ctx: commands.context.Context, args: "list[str]"):
        task = subcom_task.new_task(ctx.author.mention, " ".join(args) if args else None)
        await ctx.send(f"New Task created with Task ID {task.task_id}.")

    async def view_task(self, ctx: commands.context.Context, args: "list[str]"):
        try:
            task_id = int(args[0])
        except (ValueError, IndexError):
            raise IllegalTaskIDError()
        
        task = subcom_task.view_task(task_id)
    
        embed = task_view_embed(task)

        await ctx.send(embed=embed)

    async def view_all_tasks(self, ctx: commands.context.Context, args: "list[str]"):
        '''
        view_all_task takes an optional argument, "-a", that allows you to view the archive
        can eventually support different sorts of task i.e by ID, by due date, ...
        '''
        view_archive = len(args) > 0 and args[0] == '-a'

        if view_archive:
            tasks = subcom_task.view_all_tasks(view_archive=True)
        else:
            tasks = subcom_task.view_all_tasks(view_archive=False)

        embed = tasks_list_view_embed(tasks, view_archive)

        await ctx.send(embed=embed)
    
    async def edit_task(self, ctx: commands.context.Context, args: "list[str]"):
        if len(args) < 3 or args[0] not in ["name", "owner", "contributors", "desc", "description" "comments", "duedate"]:
            await ctx.send("Please use the command in the form `.task edit " + 
                           "[name/owner/contributors/desc/description/comments/duedate] <task_id> <arguments>`")
            return
        
        try:
            task_id = int(args[1])
        except ValueError:
            raise IllegalTaskIDError()
        
        task = subcom_task.view_task(task_id)
        
        operation = args[0]
        if operation == "name":
            task.task_name = " ".join(args[2:])
            await ctx.send(f"Task {task.task_id} renamed to {task.task_name}")
        elif operation == "owner":
            task.owner = args[2]
            await ctx.send(f"Task {task.task_id} assigned to {task.owner}.")
        elif operation == "contributors":
            task.contributors = args[2:]
            await ctx.send(f"Task {task.task_id} contributors edited.")
        elif operation == "desc" or operation == "description":
            task.description = " ".join(args[2:])
            await ctx.send(f"Task {task.task_id} description edited.")
        elif operation == "comments":
            task.comments = " ".join(args[2:])
            await ctx.send(f"Task {task.task_id} comments edited.")
        elif operation == "duedate":
            if len(args[2:]) < 3:
                await ctx.send(f"Please supply the date in format `<year> <month> <day>`")
                return
            try:
                date = datetime.date(int(args[2]), int(args[3]), int(args[4]))
                task.due_date = date
                await ctx.send(f"Task {task.task_id} due date edited to {date.isoformat()}")
            except ValueError:
                await ctx.send(f"Invalid date format supplied. Please supply the date in format `<year> <month> <day>`")

    async def archive_task(self, ctx: commands.context.Context, args: "list[str]"):
        try:
            task_id = int(args[0])
        except (ValueError, IndexError):
            raise IllegalTaskIDError()
        
        subcom_task.archive_task(task_id)

        await ctx.send(f"Task {task_id} successfully archived.")
        if archive_channel:
            embed = discord.Embed(title=f"New Archived Task: Task {task_id}", color=discord.Color.greyple())
            embed.add_field(name="Archive Date", value=subcom_task.view_task(task_id).archived_date.isoformat())
            await archive_channel.send(embed=embed)
    
    async def delete_task(self, ctx: commands.context.Context, args: "list[str]"):
        try:
            task_id = int(args[0])
        except ValueError:
            raise IllegalTaskIDError()

        subcom_task.delete_task(task_id)
        await ctx.send(f"Task {task_id} successfully deleted.")
    
    @commands.command(name="setarchivechannel")
    @commands.has_role(exec_role)
    async def set_archive_channel(self, ctx: commands.context.Context):
        global archive_channel
        archive_channel = ctx.channel
        await ctx.send(f"Archive channel set to <#{archive_channel}>.")
        
    @commands.command()
    @commands.has_any_role(exec_role, subcom_role)
    async def task(self, ctx: commands.context.Context, *args):
        if len(args) < 1 or args[0] not in ["new", "view", "viewall", "edit", "archive", "delete"]:
            await ctx.send("Please use the command in the form `.task [new/view/viewall/edit/archive/delete]`")
            return
        
        try:    
            operation = args[0]
            if operation == "new":
                await self.new_task(ctx, list(args)[1:])
            elif operation == "view":
                await self.view_task(ctx, list(args)[1:])
            elif operation == "viewall":
                await self.view_all_tasks(ctx, list(args)[1:])
            elif operation == "edit":
                await self.edit_task(ctx, list(args)[1:])
            elif operation == "archive":
                await self.archive_task(ctx, list(args)[1:])
            elif operation == "delete":
                await self.delete_task(ctx, list(args)[1:])
        except (TaskNotFoundError, IllegalTaskIDError) as e:
            await ctx.send(e)

async def setup(bot: commands.Bot):
    await bot.add_cog(SubcomTasks(bot))