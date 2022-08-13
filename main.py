import os
import discord
from discord.ext import commands

TOKEN = ""

cogs_dir = "cogs"

with open(".token", "r") as token_file:
    TOKEN = token_file.readline().strip()

command_prefix = "."
activity = discord.Game(name="Professor Layton")
bot = commands.Bot(command_prefix=command_prefix, activity=activity, help_command=None)

# load all available cogs on startup
for filename in os.listdir("cogs/"):
    if filename.endswith(".py"):
        bot.load_extension(f"{cogs_dir}.{filename[:-3]}")
        print(f"Loaded {filename}")

# command to load a cog
@bot.command()
async def load(ctx: commands.context.Context, extension):
    bot.load_extension(f"{cogs_dir}.{extension}")
    await ctx.send(f"Loaded {extension} cog")

# command to unload a cog
@bot.command()
async def unload(ctx: commands.context.Context, extension):
    bot.unload_extension(f"{cogs_dir}.{extension}")
    await ctx.send(f"Unloaded {extension} cog")

# command to reload a cog
@bot.command()
async def reload(ctx: commands.context.Context, extension):
    bot.reload_extension(f"{cogs_dir}.{extension}")
    await ctx.send(f"Reloaded {extension} cog")

bot.run(TOKEN)