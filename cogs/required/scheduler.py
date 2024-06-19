from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Scheduler(commands.Cog, AsyncIOScheduler):
    def __init__(self, bot: commands.Bot, info):
        super().__init__()
        self.start()
        self.bot = bot
        self.info = info

    async def start_puzzle(self, puzzle_name):
        puzzle = self.info.puzzles[puzzle_name]
        channel = self.bot.get_channel(puzzle.release_channel)
        channel.send(puzzle.get_text())

    def schedule_puzzle(self, puzzle_name, datetime):
        self.add_job(self.start_puzzle, "date", run_date=datetime, args=[puzzle_name])
    
async def setup(bot: commands.Bot):
    info = bot.get_cog("Info")
    await bot.add_cog(Scheduler(bot, info))