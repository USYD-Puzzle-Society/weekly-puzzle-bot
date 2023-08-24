import discord
from discord.ext import commands
from discord import app_commands
import datetime

from src import subcom_task
from src.subcom_task_errors import TaskNotFoundError
from embeds.subcom_task_embeds import task_view_embed, tasks_list_view_embed
from utils import middleware

exec_role = "Executives"
subcom_role = "Subcommittee"
archive_channel = None

class SubcomTasks(commands.GroupCog, name="task"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='new')
    @middleware.has_any_role(exec_role, subcom_role)
    async def task_new(self, interaction: discord.Interaction, task_name: str = "None"):
        """Create a new Task. Default owner is the creator of the task."""
        task = await subcom_task.new_task(interaction.user.name, task_name)
        await interaction.response.send_message(f"New Task created with Task ID {task.task_id}.")

    @app_commands.command(name='view')
    @middleware.has_any_role(exec_role, subcom_role)
    async def task_view(self, interaction: discord.Interaction, task_id: int):
        """View the details of a specific task."""
        task = await subcom_task.view_task(task_id)
        embed = task_view_embed(task)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='viewall')
    @middleware.has_any_role(exec_role, subcom_role)
    async def task_view_all(self, interaction: discord.Interaction, view_archive: bool = False):
        """View the details of all tasks."""
        tasks = await subcom_task.view_all_tasks(view_archive=view_archive)
        embed = tasks_list_view_embed(tasks, view_archive)
        await interaction.response.send_message(embed=embed)

    task_edit = app_commands.Group(name='edit', description='Commands related to editing a specific task.')
    
    @task_edit.command(name='name')
    @middleware.has_any_role(exec_role, subcom_role)
    async def task_edit_name(self, interaction: discord.Interaction, task_id: int, task_name: str):
        """Edit the name of a task."""
        task = await subcom_task.view_task(task_id)
        task.task_name = task_name
        await subcom_task.update_task(task)
        await interaction.response.send_message(f"Task {task.task_id} renamed to {task.task_name}.")
    
    @task_edit.command(name='owner')
    @middleware.has_any_role(exec_role, subcom_role)
    async def task_edit_owner(self, interaction: discord.Interaction, task_id: int, owner: discord.Member):
        """Edit the owner of a task."""
        task = await subcom_task.view_task(task_id)
        task.owner = owner.name
        await subcom_task.update_task(task)
        await interaction.response.send_message(f"Task {task.task_id} assigned to {task.owner}.")
    
    @task_edit.command(name='contributors')
    @middleware.has_any_role(exec_role, subcom_role)
    async def task_edit_contributors(self, interaction: discord.Interaction, task_id: int, 
                                     contributors: str):
        """Edit the contributors of a task."""
        task = await subcom_task.view_task(task_id)
        task.contributors = contributors.split()
        await subcom_task.update_task(task)
        await interaction.response.send_message(f"Task {task.task_id} contributors edited.")
    
    @task_edit.command(name='description')
    @middleware.has_any_role(exec_role, subcom_role)
    async def task_edit_description(self, interaction: discord.Interaction, task_id: int, description: str):
        """Edit the description of a task."""
        task = await subcom_task.view_task(task_id)
        task.description = description
        await subcom_task.update_task(task)
        await interaction.response.send_message(f"Task {task.task_id} description edited.")
    
    @task_edit.command(name='comments')
    @middleware.has_any_role(exec_role, subcom_role)
    async def task_edit_comments(self, interaction: discord.Interaction, task_id: int, comments: str):
        """Edit the comments of a task."""
        task = await subcom_task.view_task(task_id)
        task.comments = comments
        await subcom_task.update_task(task)
        await interaction.response.send_message(f"Task {task.task_id} comments edited.")
    
    @task_edit.command(name='due_date')
    @middleware.has_any_role(exec_role, subcom_role)
    async def task_edit_duedate(self, interaction: discord.Interaction, task_id: int, day: int, month: int, year: int):
        """Edit the due date of a task."""
        task = await subcom_task.view_task(task_id)
        try:
            date = datetime.datetime(year, month, day)
            task.due_date = date
            await interaction.response.send_message(f"Task {task.task_id} due date edited to {date.strftime('%Y-%m-%d')}")
        except ValueError:
            await interaction.response.send_message(f"Invalid date format supplied. Please supply the date in format `<year> <month> <day>`",
                                                    ephemeral=True)

    @app_commands.command(name='archive')
    @middleware.has_any_role(exec_role, subcom_role)
    async def task_archive(self, interaction: discord.Interaction, task_id: int):
        """Archive an existing task."""
        await subcom_task.archive_task(task_id)

        await interaction.response.send_message(f"Task {task_id} successfully archived.")
        if archive_channel:
            embed = discord.Embed(title=f"New Archived Task: Task {task_id}", color=discord.Color.greyple())
            embed.add_field(name="Archive Date", 
                            value=(await subcom_task.view_task(task_id)).archived_date.strftime('%Y-%m-%d'))
            await archive_channel.send(embed=embed)
    
    @app_commands.command(name='delete')
    @middleware.has_any_role(exec_role, subcom_role)
    async def task_delete(self, interaction: discord.Interaction, task_id: int):
        """Delete a task."""
        await subcom_task.delete_task(task_id)
        await interaction.response.send_message(f"Task {task_id} successfully deleted.")
    
    @app_commands.command(name="set_archive_channel")
    @middleware.has_any_role(exec_role, subcom_role)
    async def set_archive_channel(self, interaction: discord.Interaction):
        """Set the archive channel to the current channel."""
        global archive_channel
        archive_channel = interaction.channel
        await interaction.response.send_message(f"Archive channel set to <#{archive_channel}>.")
    
    async def cog_app_command_error(self, interaction: discord.Interaction, 
                                    error: discord.app_commands.AppCommandError):
        if isinstance(error, TaskNotFoundError):
            await interaction.response.send_message(error, ephemeral=True)
        else:
            print(error)


async def setup(bot: commands.Bot):
    await bot.add_cog(SubcomTasks(bot))