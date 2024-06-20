import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.help_commands = [
            "/help setup\n\n",
            "/help show\n\n",
            "/help reactions"
        ]
        self.help_commands_desc = [
            "Commands for setting up info for puzzle announcements\n\n",
            "Commands for showing the puzzle announcements\n\n",
            "Different reaction commands"
        ]

        self.help_setup = [
            "/role <puzzle_name> <role_name>\n\n",
            "/channel <puzzle_name> <channel_id>\n\n\n",
            "/time <puzzle_name> <date> <time>\n\n\n",
            "/week <puzzle_name> <week>\n\n\n",
            "/images <puzzle_name>\n\n\n",
            "/links <puzzle_name> <submission_link> <interactive_link>\n\n"
        ]
        self.help_setup_desc = [
            "Sets the role for the specified puzzle.\n\n",
            "Sets the release channel for the specified puzzle.\n\n",
            "Sets the release time for the specified puzzle.\n\n",
            "Sets the week number for the specified puzzle.\n\n",
            "Sets the image URLs for the specified puzzle.\n\n",
            "Sets the submission and interactive links for the specified puzzle.\n\n",
        ]
        
        self.help_show = [
            "/show puzzle <puzzle_name>\n\n",
        ]
        self.help_show_desc = [
            "Shows the release time, content, and images of the specified puzzle. It will also show the role and the release channel.\n\n",
        ]

        self.help_reactions = [
            ".bird\n\n",
            ".dog\n\n",
            ".wut\n\n",
            ".stare\n\n\n",
            ".aa[aaaaaaaa]\n\n",
            ".tear\n\n"
            ".pansive\n\n",
            ".devious\n\n\n",
            ".rubidance\n\n\n",
            ".pint\n\n\n",
            ".pills\n\n",
            ".sus\n\n",
            ".gunpoint [optional tag/text]\n\n",
            ".bonk [optional tag/text]\n\n",
            ".pfp [optional tag]\n\n\n",
            ".colour [colour]\n\n\n",
            ".phc [number]"
        ]
        self.help_reactions_desc = [
            "bird\n\n",
            "dog\n\n",
            "wut\n\n",
            "when class is almost over but some kid reminds the teacher about homework\n\n",
            "when you lol irl\n\n",
            "when fifi deletes your pills\n\n"
            "when you're bread and also sad\n\n",
            "when your dad asks if you ate the rest of the hummus and you say no but you really did\n\n",
            "when you're happy and you know it and you're a cube and you want to show it\n\n",
            "when someone says they don't want to solve puzzles at a bar\n\n",
            "take the pills :gun:\n\n",
            "sus\n\n"
            "Deals light Gun damage 1-3 times to one foe.\n\n",
            "Deals severe Almighty damage to one foe.\n\n",
            "Reveals in clarity the displayed persona of an individual.\n\n",
            "displays the colour specified. can be hexadecimal or words\n\n",
            "Use command without a number to list all events from Puzzle Hunt Calendar. Use command with number to view description for specific event."
        ]

    def get_commands_embed(self) -> discord.Embed:
        embed = discord.Embed(title="Command Categories", color=discord.Colour.greyple())
        embed.add_field(name="Category", value="".join(self.help_commands), inline=True)
        embed.add_field(name="Description", value="".join(self.help_commands_desc), inline=True)
        return embed

    def get_setup_embed(self) -> discord.Embed:
        embed = discord.Embed(title="Setup", color=discord.Colour.blue())
        embed.add_field(name="Command", value="".join(self.help_setup), inline=True)
        embed.add_field(name="Description", value="".join(self.help_setup_desc), inline=True)
        return embed
    
    def get_show_embed(self) -> discord.Embed:
        embed = discord.Embed(title="Show", color=discord.Colour.dark_gold())
        embed.add_field(name="Command", value="".join(self.help_show), inline=True)
        embed.add_field(name="Description", value="".join(self.help_show_desc), inline=True)
        return embed

    def get_reactions_embed(self) -> discord.Embed:
        embed = discord.Embed(title="Reactions", color=discord.Colour.teal())
        embed.add_field(name="Command", value="".join(self.help_reactions), inline=True)
        embed.add_field(name="Description", value="".join(self.help_reactions_desc), inline=True)
        return embed

    @discord.app_commands.command(
        name="help"
    )
    async def help(self, interaction: discord.Interaction, command: str = None):
        if not any(role.name == "Executives" for role in interaction.user.roles):
            await interaction.response.send_message(embed=self.get_reactions_embed())
            return

        if not command:
            await interaction.response.send_message(embed=self.get_commands_embed())
            return

        embeds = {
            "setup": self.get_setup_embed,
            "show": self.get_show_embed,
            "reactions": self.get_reactions_embed
        }

        if not command in embeds:
            await interaction.response.send_message(f"{command.lower().capitalize()} is not a valid command category.")
            return

        await interaction.response.send_message(embed=embeds[command.lower()]())

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot), guild=discord.Object(1153319575048437833))