from discord.ext import commands
import discord
from info import Info

class Top3WeeklyPuz(commands.Cog):
    def __init__(self, bot: commands.Bot, info: Info):
        self.bot = bot
        self.info_obj = info
        self.watch_channel_id = None

    @commands.command()
    @commands.has_role("Executives")
    async def weekly_puz_set_channel(self, ctx: commands.Context):
        self.watch_channel_id = ctx.channel.id
        await ctx.send(f"Weekly Puzzle watch channel set to {ctx.channel.name}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot and message.content == 'from webhook: top 3 taken' \
            and message.channel.id == self.watch_channel_id:
            await self.bot.get_channel(self.info_obj.info["minipuzz"]["channel_id"]).send("Hints are enabled!")
        
async def setup(bot: commands.Bot):
    info = Info()
    await bot.add_cog(Top3WeeklyPuz(bot, info))
