from discord.ext import commands

FORM_API = ""

class WeeklyPuz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != 1100077444922359959:
            return
        await self.bot.get_channel(994948949536407612).send("Hints are enabled!")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(WeeklyPuz(bot))
