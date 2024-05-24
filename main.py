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
    name="startup"
)
@commands.has_role(exec_id)
async def startup(interaction: discord.Interaction):
    await interaction.response.defer()
    for filename in os.listdir("cogs/"):
        if filename.endswith(".py"):
            await bot.load_extension(f"{cogs_dir}.{filename[:-3]}")
            print(f"Loaded {filename}")
    await bot.tree.sync(guild=guild)
    await interaction.followup.send("Loaded all cogs")

# command to load a cog
@bot.tree.command(
    name="load"
)
@commands.has_role(exec_id)
async def load(interaction: discord.Interaction, extension: str):
    await interaction.response.defer()
    await bot.load_extension(f"{cogs_dir}.{extension}")
    await bot.tree.sync(guild=guild)
    await interaction.followup.send(f"Loaded {extension} cog")

# command to unload a cog
@bot.tree.command(
    name="unload"
)
@commands.has_role(exec_id)
async def unload(interaction: discord.Interaction, extension: str):
    await interaction.response.defer()
    await bot.unload_extension(f"{cogs_dir}.{extension}")
    await bot.tree.sync(guild=guild)
    await interaction.followup.send(f"Unloaded {extension} cog")

# command to reload a cog
@bot.tree.command(
    name="reload"
)
@commands.has_role(exec_id)
async def reload(interaction: discord.Interaction, extension: str):
    await interaction.response.defer()
    await bot.reload_extension(f"{cogs_dir}.{extension}")
    await bot.tree.sync(guild=guild)
    await interaction.followup.send(f"Reloaded {extension} cog")

bot.run(TOKEN)