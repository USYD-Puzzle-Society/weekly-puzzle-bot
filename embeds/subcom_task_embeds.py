import discord

from classes.Task import Task

def task_view_embed(task: Task) -> discord.Embed:
    embed = discord.Embed(title=f"Task Details for Task {task.task_id}", color=discord.Color.greyple())
    embed.add_field(name="Task ID", value=task.task_id, inline=False)
    embed.add_field(name="Task Name", value=task.task_name, inline=False)
    embed.add_field(name="Owner", value=task.owner, inline=False)
    embed.add_field(name="Contributors", value=task.contributors_to_str(), inline=False)
    embed.add_field(name="Creation Date", value=task.creation_date.isoformat())
    embed.add_field(name="Due Date", value=task.due_date.isoformat(), inline=False)
    embed.add_field(name="Description", value=task.description, inline=False)
    embed.add_field(name="Comments", value=task.comments, inline=False)
    if task.archived:
        embed.add_field(name="Archive Date", value=task.archived_date.isoformat(), inline=False)
    return embed

def tasks_list_view_embed(tasks: "list[Task]", view_archive) -> discord.Embed:
        if view_archive:
            title = "All Archived Tasks"
        else:
            title = "All Active Tasks"

        embed = discord.Embed(title=title, color=discord.Color.greyple())
        values = list(map(list, zip(*[task.summary_to_tuple() for task in tasks]))) # cursed

        if not values:
            embed.add_field(name="Tasks", value="")
            embed.add_field(name="Owner", value="")
            embed.add_field(name="Due Date", value="")
        else:
            embed.add_field(name="Tasks", value="\n".join((['. '.join(x) for x in zip([str(x) for x in values[0]], values[1])])))
            embed.add_field(name="Owner", value="\n".join(values[2]))
            embed.add_field(name="Due Date", value="\n".join([time.isoformat() for time in values[3]] ))
        
        return embed