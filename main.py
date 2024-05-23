import os
import discord
from discord.ext import commands

with open(".token", "r") as token_file:
    TOKEN = token_file.readline().strip()

guild = discord.Object(1153319575048437833)
exec_id = "Executives"
cogs_dir = "cogs"
intents = discord.Intents.all()

bot = commands.Bot(command_prefix=".", help_command=None, intents=intents)

# load all available cogs on startup
@bot.tree.command(
    name="startup",
    guild=guild
)
@commands.has_role(exec_id)
async def startup(ctx: commands.context.Context):
    for filename in os.listdir("cogs/"):
        if filename.endswith(".py"):
            await bot.load_extension(f"{cogs_dir}.{filename[:-3]}")
            print(f"Loaded {filename}")
    await ctx.channel.send(f"Loaded all cogs")

# command to load a cog
@bot.tree.command(
    name="load",
    guild=guild
)
@commands.has_role(exec_id)
async def load(ctx: commands.context.Context, extension: str):
    await bot.load_extension(f"{cogs_dir}.{extension}")
    await ctx.send(f"Loaded {extension} cog")

# command to unload a cog
@bot.tree.command(
    name="unload",
    guild=guild
)
@commands.has_role(exec_id)
async def unload(ctx: commands.context.Context, extension: str):
    await bot.unload_extension(f"{cogs_dir}.{extension}")
    await ctx.send(f"Unloaded {extension} cog")

# command to reload a cog
@bot.tree.command(
    name="reload",
    guild=guild
)
@commands.has_role(exec_id)
async def reload(ctx: commands.context.Context, extension: str):
    await bot.reload_extension(f"{cogs_dir}.{extension}")
    await ctx.send(f"Reloaded {extension} cog")

bot.run(TOKEN)