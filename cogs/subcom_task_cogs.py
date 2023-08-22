import discord
from discord.ext import commands
from discord import app_commands
import datetime

from classes.Task import Task
from src import subcom_task
from src.subcom_task_errors import TaskNotFoundError
from embeds.subcom_task_embeds import task_view_embed, tasks_list_view_embed

exec_role = "Executives"
subcom_role = "Subcommittee"
archive_channel = None

class SubcomTasks(commands.GroupCog, name="task"):
    def __init__(self, bot):
        self.bot = bot

    async def has_appropriate_role(interaction: discord.Interaction):
        roles = [role.name for role in interaction.user.roles]
        return exec_role in roles or subcom_role in roles

    @app_commands.command(name='new')
    @app_commands.check(has_appropriate_role)
    async def task_new(self, interaction: discord.Interaction, task_name: str = "None"):
        """Create a new Task. Default owner is the creator of the task."""
        task = subcom_task.new_task(interaction.user.mention, task_name)
        await interaction.response.send_message(f"New Task created with Task ID {task.task_id}.")

    @app_commands.command(name='view')
    @app_commands.check(has_appropriate_role)
    async def task_view(self, interaction: discord.Interaction, task_id: int):
        """View the details of a specific task."""
        task = subcom_task.view_task(task_id)
        embed = task_view_embed(task)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='viewall')
    @app_commands.check(has_appropriate_role)
    async def task_view_all(self, interaction: discord.Interaction, view_archive: bool = False):
        """View the details of all tasks."""
        tasks = subcom_task.view_all_tasks(view_archive=view_archive)
        embed = tasks_list_view_embed(tasks, view_archive)
        await interaction.response.send_message(embed=embed)

    task_edit = app_commands.Group(name='edit', description='Commands related to editing a specific task.')
    
    @task_edit.command(name='name')
    @app_commands.check(has_appropriate_role)
    async def task_edit_name(self, interaction: discord.Interaction, task_id: int, task_name: str):
        """Edit the name of a task."""
        task = subcom_task.view_task(task_id)
        task.task_name = task_name
        subcom_task.update_task(task)
        await interaction.response.send_message(f"Task {task.task_id} renamed to {task.task_name}.")
    
    @task_edit.command(name='owner')
    @app_commands.check(has_appropriate_role)
    async def task_edit_owner(self, interaction: discord.Interaction, task_id: int, owner: discord.Member):
        """Edit the owner of a task."""
        task = subcom_task.view_task(task_id)
        task.owner = owner.name
        subcom_task.update_task(task)
        await interaction.response.send_message(f"Task {task.task_id} assigned to {task.owner}.")
    
    @task_edit.command(name='contributors')
    @app_commands.check(has_appropriate_role)
    async def task_edit_contributors(self, interaction: discord.Interaction, task_id: int, 
                                     contributors: str):
        """Edit the contributors of a task."""
        task = subcom_task.view_task(task_id)
        task.contributors = contributors.split()
        subcom_task.update_task(task)
        await interaction.response.send_message(f"Task {task.task_id} contributors edited.")
    
    @task_edit.command(name='description')
    @app_commands.check(has_appropriate_role)
    async def task_edit_description(self, interaction: discord.Interaction, task_id: int, description: str):
        """Edit the description of a task."""
        task = subcom_task.view_task(task_id)
        task.description = description
        subcom_task.update_task(task)
        await interaction.response.send_message(f"Task {task.task_id} description edited.")
    
    @task_edit.command(name='comments')
    @app_commands.check(has_appropriate_role)
    async def task_edit_comments(self, interaction: discord.Interaction, task_id: int, comments: str):
        """Edit the comments of a task."""
        task = subcom_task.view_task(task_id)
        task.comments = comments
        subcom_task.update_task(task)
        await interaction.response.send_message(f"Task {task.task_id} comments edited.")
    
    @task_edit.command(name='due_date')
    @app_commands.check(has_appropriate_role)
    async def task_edit_duedate(self, interaction: discord.Interaction, task_id: int, day: int, month: int, year: int):
        """Edit the due date of a task."""
        task = subcom_task.view_task(task_id)
        try:
            date = datetime.date(year, month, day)
            task.due_date = date
            await interaction.response.send_message(f"Task {task.task_id} due date edited to {date.isoformat()}")
        except ValueError:
            await interaction.response.send_message(f"Invalid date format supplied. Please supply the date in format `<year> <month> <day>`",
                                                    ephemeral=True)

    @app_commands.command(name='archive')
    @app_commands.check(has_appropriate_role)
    async def task_archive(self, interaction: discord.Interaction, task_id: int):
        """Archive an existing task."""
        subcom_task.archive_task(task_id)

        await interaction.response.send_message(f"Task {task_id} successfully archived.")
        if archive_channel:
            embed = discord.Embed(title=f"New Archived Task: Task {task_id}", color=discord.Color.greyple())
            embed.add_field(name="Archive Date", value=subcom_task.view_task(task_id).archived_date.isoformat())
            await archive_channel.send(embed=embed)
    
    @app_commands.command(name='delete')
    @app_commands.check(has_appropriate_role)
    async def task_delete(self, interaction: discord.Interaction, task_id: int):
        """Delete a task."""
        subcom_task.delete_task(task_id)
        await interaction.response.send_message(f"Task {task_id} successfully deleted.")
    
    @app_commands.command(name="set_archive_channel")
    @app_commands.check(has_appropriate_role)
    async def set_archive_channel(self, interaction: discord.Interaction):
        """Set the archive channel to the current channel."""
        global archive_channel
        archive_channel = interaction.channel
        await interaction.response.send_message(f"Archive channel set to <#{archive_channel}>.")
    
    async def cog_app_command_error(self, interaction: discord.Interaction, 
                                    error: discord.app_commands.AppCommandError):
        if isinstance(error, discord.app_commands.CheckFailure):
            await interaction.response.send_message("You don't have the permission to execute this command!", ephemeral=True)
        else:
            print(error)


async def setup(bot: commands.Bot):
    await bot.add_cog(SubcomTasks(bot))