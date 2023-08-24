import discord
from datetime import datetime
from typing import List

from classes.Task import Task

def task_view_embed(task: Task) -> discord.Embed:
    embed = discord.Embed(title=f"Task Details for Task {task.task_id}", color=discord.Color.greyple())
    embed.add_field(name="Task ID", value=task.task_id, inline=False)
    embed.add_field(name="Task Name", value=task.task_name, inline=False)
    embed.add_field(name="Owner", value=task.owner, inline=False)
    embed.add_field(name="Contributors", value=', '.join(task.contributors), inline=False)
    embed.add_field(name="Creation Date", value=task.creation_date.strftime('%Y-%m-%d'))
    embed.add_field(name="Due Date", value=task.due_date.strftime('%Y-%m-%d') if task.due_date else 'None', inline=False)
    embed.add_field(name="Description", value=task.description, inline=False)
    embed.add_field(name="Comments", value=task.comments, inline=False)
    if task.archived:
        embed.add_field(name="Archive Date", value=task.archived_date.strftime('%Y-%m-%d'), inline=False)
    return embed

def tasks_list_view_embed(tasks: List[Task], view_archive: bool) -> discord.Embed:
    if view_archive:
        title = "All Archived Tasks"
    else:
        title = "All Active Tasks"

    embed = discord.Embed(title=title, color=discord.Color.greyple())

    values = [format_task_summary(*task.get_summary()) for task in tasks]

    embed.description = '\n'.join(values)
    
    return embed

def format_task_summary(task_id: int, task_name: str, owner: str, due_date: datetime):
    due_date = due_date.strftime('%Y-%m-%d') if due_date else 'None'
    task = f'{task_id}. {task_name}'
    task_name_width = 40
    owner_width = 20
    due_date_width = 20

    task_name_formatted = f"{task[:task_name_width-3]}..." if len(task) > task_name_width else task.ljust(task_name_width)
    owner_formatted = f"{owner[:owner_width-3]}..." if len(owner) > owner_width else owner.ljust(owner_width)
    due_date_formatted = f"{due_date[:due_date_width-3]}..." if len(due_date) > due_date_width else due_date.ljust(due_date_width)

    formatted_string = f"{task_name_formatted}{owner_formatted}{due_date_formatted}"

    return formatted_string