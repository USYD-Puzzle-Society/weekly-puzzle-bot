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
@bot.event
@commands.has_role(exec_id)
async def on_ready():
    for filename in os.listdir("cogs/"):
        if filename.endswith(".py"):
            await bot.load_extension(f"{cogs_dir}.{filename[:-3]}")
            print(f"Loaded {filename}")

# command to load a cog
@bot.command()
@commands.has_role(exec_id)
async def load(ctx: commands.context.Context, extension):
    await bot.load_extension(f"{cogs_dir}.{extension}")
    await ctx.send(f"Loaded {extension} cog")

# command to unload a cog
@bot.command()
@commands.has_role(exec_id)
async def unload(ctx: commands.context.Context, extension):
    await bot.unload_extension(f"{cogs_dir}.{extension}")
    await ctx.send(f"Unloaded {extension} cog")

# command to reload a cog
@bot.command()
@commands.has_role(exec_id)
async def reload(ctx: commands.context.Context, extension):
    await bot.reload_extension(f"{cogs_dir}.{extension}")
    await ctx.send(f"Reloaded {extension} cog")

# command to sync the command trees either globally, or to the current guild
@bot.command()
@commands.has_role(exec_id)
async def sync(ctx: commands.context.Context, globally: bool = False):
    if globally:
        await bot.tree.sync()
    else:
        ctx.bot.tree.copy_global_to(guild=ctx.guild)
        await bot.tree.sync(guild=ctx.guild)

    await ctx.send(
        f"Synced commands {'globally' if globally else 'to the current guild.'}"
    )

bot.run(TOKEN)