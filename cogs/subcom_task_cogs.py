import discord
from discord.ext import commands
import datetime

from classes.Task import Task
from classes.ArchivedTask import ArchivedTask
from src import subcom_task

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
        if not args:
            await ctx.send("You must provide a Task ID for viewing!")
            return
        
        to_be_viewed = subcom_task.view_task(args[0])

        if to_be_viewed:
            embed = discord.Embed(title=f"Task Details for Task {to_be_viewed.task_id}", color=discord.Color.greyple())
            embed.add_field(name="Task ID", value=to_be_viewed.task_id, inline=False)
            embed.add_field(name="Task Name", value=to_be_viewed.task_name, inline=False)
            embed.add_field(name="Owner", value=to_be_viewed.owner, inline=False)
            embed.add_field(name="Contributors", value=to_be_viewed.contributors_to_str(), inline=False)
            embed.add_field(name="Creation Date", value=to_be_viewed.creation_date.isoformat())
            embed.add_field(name="Due Date", value=to_be_viewed.due_date.isoformat(), inline=False)
            embed.add_field(name="Description", value=to_be_viewed.description, inline=False)
            embed.add_field(name="Comments", value=to_be_viewed.comments, inline=False)
            if isinstance(to_be_viewed, ArchivedTask):
                embed.add_field(name="Archive Date", value=to_be_viewed.archived_date.isoformat(), inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Task {args[0]} not found!")

    async def view_all_tasks(self, ctx: commands.context.Context, args: "list[str]"):
        '''
        view_all_task takes an optional argument, "-a", that allows you to view the archive
        can eventually support different sorts of task i.e by ID, by due date, ...
        '''

        if len(args) > 0 and args[0] == "-a":
            title = "All Archived Tasks"
            view_list = self.archives
        else:
            title = "All Active Tasks"
            view_list = self.tasks

        embed = discord.Embed(title=title, color=discord.Color.greyple())
        values = list(map(list, zip(*[task.summary_to_tuple() for task in view_list]))) # cursed

        if not values:
            embed.add_field(name="Tasks", value="")
            embed.add_field(name="Owner", value="")
            embed.add_field(name="Due Date", value="")
        else:
            embed.add_field(name="Tasks", value="\n".join((['. '.join(x) for x in zip([str(x) for x in values[0]], values[1])])))
            embed.add_field(name="Owner", value="\n".join(values[2]))
            embed.add_field(name="Due Date", value="\n".join([time.isoformat() for time in values[3]] ))

        await ctx.send(embed=embed)
    
    async def edit_task(self, ctx: commands.context.Context, args: "list[str]"):
        if len(args) < 3 or args[0] not in ["name", "owner", "contributors", "desc", "description" "comments", "duedate"]:
            await ctx.send("Please use the command in the form `.task edit " + 
                           "[name/owner/contributors/desc/description/comments/duedate] <task_id> <arguments>`")
            return
        task = self.find_task(args[1])
        if not task:
            await ctx.send(f"Task {args[1]} not found!")
            return
        
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
            except:
                await ctx.send(f"Invalid date format supplied. Please supply the date in format `<year> <month> <day>`")

    async def archive_task(self, ctx: commands.context.Context, args: "list[str]"):
        if not args:
            await ctx.send("You must provide a Task ID for archiving!")
            return
        subcom_task.archive_task(args[0])

        await ctx.send(f"Task {args[0]} successfully archived.")
        if archive_channel:
            embed = discord.Embed(title=f"New Archived Task: Task {args[0].task_id}", color=discord.Color.greyple())
            embed.add_field(name="Archive Date", value=subcom_task.view_task(args[0]).archived_date.isoformat())
            await archive_channel.send(embed=embed)
    
    async def delete_task(self, ctx: commands.context.Context, args: "list[str]"):
        if not args:
            await ctx.send("You must provide a Task ID for deletion!")
            return
        result = subcom_task.delete_task(args[0])
        if result:
            await ctx.send(f"Task {args[0]} successfully deleted.")
        else:
            await ctx.send(f"Task {args[0]} not found!")
    
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

async def setup(bot: commands.Bot):
    await bot.add_cog(SubcomTasks(bot))