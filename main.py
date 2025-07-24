import os
import discord
from discord.ext import commands

TOKEN = ""

exec_id = "Executives"

cogs_dir = "cogs"

with open(".token", "r") as token_file:
    TOKEN = token_file.readline().strip()

command_prefix = "."
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=command_prefix, help_command=None, intents=intents)


# Function for loading all cogs
async def load_all_cogs():
    for filename in os.listdir("cogs/"):
        if filename.endswith(".py"):
            await bot.load_extension(f"{cogs_dir}.{filename[:-3]}")
            print(f"Loaded {filename}")
    print("Loaded all cogs")

# Run on bot startup
@commands.Cog.listener()
async def on_ready(self):
    await self.bot.wait_until_ready()
    await load_all_cogs()

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


@bot.command()
async def sync(ctx: commands.context.Context):
    try:
        bot.tree.copy_global_to(guild=ctx.guild)
        synced = await bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(e)


@bot.command()
async def clear(ctx: commands.context.Context):
    bot.tree.clear_commands(guild=ctx.guild)

    try:
        await bot.tree.sync()
        await ctx.send("Commands cleared.")
    except Exception as e:
        print(e)


bot.run(TOKEN)
