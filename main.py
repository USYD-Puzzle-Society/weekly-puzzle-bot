import os
import discord
from discord.ext import commands

TOKEN = ""

exec_id = "Executives"

cogs_dir = "cogs"

with open(".token", "r") as token_file:
    TOKEN = token_file.readline().strip()

command_prefix = "."
activity = discord.Game(name="Professor Layton")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=command_prefix, activity=activity, help_command=None, intents=intents)

# load all available cogs on startup
@bot.command()
@commands.has_role(exec_id)
async def startup(ctx: commands.context.Context):
    for filename in os.listdir("cogs/"):
        if filename.endswith(".py"):
            bot.load_extension(f"{cogs_dir}.{filename[:-3]}")
            print(f"Loaded {filename}")
    await ctx.send(f"Loaded all cogs")

# command to load a cog
@bot.command()
@commands.has_role(exec_id)
async def load(ctx: commands.context.Context, extension):
    bot.load_extension(f"{cogs_dir}.{extension}")
    await ctx.send(f"Loaded {extension} cog")

# command to unload a cog
@bot.command()
@commands.has_role(exec_id)
async def unload(ctx: commands.context.Context, extension):
    bot.unload_extension(f"{cogs_dir}.{extension}")
    await ctx.send(f"Unloaded {extension} cog")

# command to reload a cog
@bot.command()
@commands.has_role(exec_id)
async def reload(ctx: commands.context.Context, extension):
    bot.reload_extension(f"{cogs_dir}.{extension}")
    await ctx.send(f"Reloaded {extension} cog")

bot.run(TOKEN)