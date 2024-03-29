import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.help_commands = [
            ".help setup\n\n",
            ".help show\n\n",
            ".help start\n\n",
            ".help stop\n\n",
            ".help reactions"
        ]
        self.help_commands_desc = [
            "Commands for setting up info for puzzle announcements\n\n",
            "Commands for showing the current puzzle announcement text\n\n",
            "Commands for starting the release for puzzle announcements\n\n",
            "Commands for stopping puzzle announcement release\n\n",
            "Different reaction commands"
        ]

        self.help_setup = [
            ".setrc\n\n",
            ".setrctime\n\n"
            ".setminipuzz\n\n",
            ".setminipuzztime\n\n",
            ".setcrossword\n\n",
            ".setcrosswordtime\n\n",
            ".setsudoku\n\n",
            ".setsudokutime\n\n"
            ".setciyk\n\n",
            ".setciyktime\n\n"
        ]
        self.help_setup_desc = [
            "Sets up rebus and cryptic.\n\n",
            "Sets up the release time for the rebus and cryptic\n\n",
            "Sets up the minipuzzle\n\n",
            "Changes the release time of the minipuzzle.\n\n",
            "Sets up the crossword\n\n",
            "Sets up the release time for the crossword\n\n",
            "Sets up the sudoku\n\n",
            "Sets up the release time for the sudoku\n\n",
            "Sets up the CIYK announcement.\n\n",
            "Changes the release time of CIYK.\n\n",
        ]
        
        self.help_show = [
            "showrc\n\n",
            ".showminipuzz\n\n",
            ".showcrossword\n\n",
            ".showsudoku\n\n",
            ".showciyk"
        ]
        self.help_show_desc = [
            "Shows time and content of the release for rebus and cryptic\n\n",
            "Shows time and content of the release for the puzzles.\n\n",
            "Shows time and content of the release for crossword\n\n",
            "Shows time and content of the release for sudoku\n\n",
            "Shows time and content of the release for CIYK"
        ]
        
        self.help_start = [
            ".start puzz\n\n\n",
            ".start crossword\n\n\n",
            ".start sudoku\n\n\n",
            ".start ciyk"
        ]
        self.help_start_desc = [
            "Starts the release for the puzzles. This command must be used in order for the puzzles to be released.\n\n",
            "Starts the release for crossword. This command must be used in order for the crossword to be released.\n\n",
            "Starts the release for sudoku. This command must be used in order for the sudoku to be released.\n\n",
            "Starts the release for CIYK. This command must be used in order for CIYK to be released."
        ]
        
        self.help_stop = [
            ".stoppuzz [id]"
        ]
        self.help_stop_desc = [
            "Stops the announcement with the given ID from releasing."
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
        embed_msg = discord.Embed(title="Command Categories", color=discord.Colour.greyple())

        embed_msg.add_field(name="Category", value="".join(self.help_commands), inline=True)
        embed_msg.add_field(name="Description", value="".join(self.help_commands_desc), inline=True)

        return embed_msg

    def get_setup_embed(self) -> discord.Embed:
        embed_msg = discord.Embed(title="Setup", color=discord.Colour.blue())

        embed_msg.add_field(name="Command", value="".join(self.help_setup), inline=True)
        embed_msg.add_field(name="Description", value="".join(self.help_setup_desc), inline=True)

        return embed_msg
    
    def get_show_embed(self) -> discord.Embed:
        embed_msg = discord.Embed(title="Show", color=discord.Colour.dark_gold())

        embed_msg.add_field(name="Command", value="".join(self.help_show), inline=True)
        embed_msg.add_field(name="Description", value="".join(self.help_show_desc), inline=True)

        return embed_msg
    
    def get_start_embed(self) -> discord.Embed:
        embed_msg = discord.Embed(title="Start", color=discord.Colour.green())

        embed_msg.add_field(name="Command", value="".join(self.help_start), inline=True)
        embed_msg.add_field(name="Description", value="".join(self.help_start_desc), inline=True)

        return embed_msg

    def get_stop_embed(self) -> discord.Embed:
        embed_msg = discord.Embed(title="Stop", color=discord.Colour.red())

        embed_msg.add_field(name="Command", value="".join(self.help_stop), inline=True)
        embed_msg.add_field(name="Description", value="".join(self.help_stop_desc), inline=True)

        return embed_msg

    def get_reactions_embed(self) -> discord.Embed:
        embed_msg = discord.Embed(title="Reactions", color=discord.Colour.teal())

        embed_msg.add_field(name="Command", value="".join(self.help_reactions), inline=True)
        embed_msg.add_field(name="Description", value="".join(self.help_reactions_desc), inline=True)

        return embed_msg

    @commands.command()
    async def help(self, ctx: commands.context.Context):
        user_roles = ctx.author.roles

        is_exec = False
        for role in user_roles:
            if "Executives" == role.name:
                is_exec = True
                break
        
        if not is_exec:
            embed_msg = self.get_reactions_embed()
            await ctx.send(embed=embed_msg)

            return
        
        else:
            arguments = ctx.message.content.split()[1:]

            get_embeds = {
                "setup": self.get_setup_embed,
                "show": self.get_show_embed,
                "start": self.get_start_embed,
                "stop": self.get_stop_embed,
                "reactions": self.get_reactions_embed
            }

            if 0 == len(arguments):
                embed_msg = self.get_commands_embed()

                await ctx.send(embed=embed_msg)
            else:
                argument = arguments[0]

                try:
                    embed_msg = get_embeds[argument.lower()]()
                    await ctx.send(embed=embed_msg)
                except KeyError:
                    await ctx.send(f"{argument} is not a valid command category.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))