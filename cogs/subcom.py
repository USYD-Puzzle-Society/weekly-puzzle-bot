import discord
from discord.ext import commands
import asyncio
from classes.Task import Task, from_dict
import datetime
import os
import json

exec_role = "Executives"
subcom_role = "Subcommittee"

class SubcomTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tasks: list[Task] = []
        self.tasks_fn = "subcom_tasks.json"

        if os.path.exists(self.tasks_fn):
            with open(self.tasks_fn, "r") as t:
                temp = json.load(t)
                for task in temp:
                    self.tasks.append(from_dict(task))
        

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
    async def new_task(self, ctx: commands.context.Context, args: "list[str]"):
        task = Task(args[0] if args else "None", ctx.author.mention)
        self.tasks.append(task)
        with open(self.tasks_fn, "w") as t:
            json.dump([task.to_dict() for task in self.tasks], t)
        await ctx.send(f"New Task created with Task ID {task.task_id}")

    async def view_task(self, ctx: commands.context.Context, args: "list[str]"):
        if not args:
            await ctx.send("You must provide a Task ID for viewing!")
            return
        to_be_viewed = self.find_task(args[0])
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
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Task {args[0]} not found!")

    async def view_all_tasks(self, ctx: commands.context.Context, args: "list[str]"):
        '''
        view_all_task ignore all args given to it.
        can eventually support different sorts of task i.e by ID, by due date, ...
        '''

        embed = discord.Embed(title="All Active Tasks", color=discord.Color.greyple())
        values = list(map(list, zip(*[task.summary_to_tuple() for task in self.tasks]))) # cursed
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
        if len(args) < 3 or args[0] not in ["name", "owner", "contributors", "desc", "comments", "duedate"]:
            await ctx.send("Please use the command in the form `.task edit " + 
                           "[name/owner/contributors/desc/comments/duedate] <task_id> <arguments>`")
            return
        task = self.find_task(args[1])
        if not task:
            await ctx.send(f"Task {args[1]} not found!")
            return
        
        operation = args[0]
        if operation == "name":
            task.task_name = args[2]
            await ctx.send(f"Task {task.task_id} renamed to {args[2]}")
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

        with open(self.tasks_fn, "w") as t:
            json.dump([task.to_dict() for task in self.tasks], t)

    async def delete_task(self, ctx: commands.context.Context, args: "list[str]"):
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
        if len(args) < 1 or args[0] not in ["new", "view", "viewall", "edit", "delete"]:
            await ctx.send("Please use the command in the form `.task [new/view/viewall/edit/delete]`")
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
        elif operation == "delete":
            await self.delete_task(ctx, list(args)[1:])

async def setup(bot: commands.Bot):
    await bot.add_cog(SubcomTasks(bot))