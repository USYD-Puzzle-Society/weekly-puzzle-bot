import os
import discord
from discord.ext import commands

with open(".token", "r") as token_file:
    TOKEN = token_file.readline().strip()

guild = discord.Object(1267016354012336138)
bot = commands.Bot(command_prefix=".", help_command=None, intents=discord.Intents.all())

# load all available cogs on startup
@bot.tree.command(
    name="startup",
    description="Loads all available cogs on startup."
)
@commands.has_role("Executives")
async def startup(interaction: discord.Interaction):
    for filename in os.listdir("cogs/optional"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.optional.{filename[:-3]}")
            print(f"Loaded {filename}")
    await interaction.response.send_message("Loaded all cogs")
    await bot.tree.sync(guild=guild)

# command to load a cog
@bot.tree.command(
    name="load",
    description="Loads a specified cog."
)
@commands.has_role("Executives")
async def load(interaction: discord.Interaction, extension: str):
    await bot.load_extension(f"cogs.optional.{extension}")
    await interaction.response.send_message(f"Loaded {extension} cog")
    await bot.tree.sync(guild=guild)

# command to unload a cog
@bot.tree.command(
    name="unload",
    description="Unloads a specified cog."
)
@commands.has_role("Executives")
async def unload(interaction: discord.Interaction, extension: str):
    await bot.unload_extension(f"cogs.optional.{extension}")
    await interaction.response.send_message(f"Unloaded {extension} cog")
    await bot.tree.sync(guild=guild)

# command to reload a cog
@bot.tree.command(
    name="reload",
    description="Reloads a specified cog."
)
@commands.has_role("Executives")
async def reload(interaction: discord.Interaction, extension: str):
    await bot.reload_extension(f"cogs.optional.{extension}")
    await interaction.response.send_message(f"Reloaded {extension} cog")
    await bot.tree.sync(guild=guild)

# command to load required cogs, the order is important
@bot.event
async def on_ready():
    for filename in sorted(os.listdir("cogs/required")):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.required.{filename[:-3]}")
            print(f"Loaded {filename}")

bot.run(TOKEN)