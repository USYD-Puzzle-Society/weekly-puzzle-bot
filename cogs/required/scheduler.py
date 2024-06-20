import datetime
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import JobLookupError


class PuzzleScheduler(commands.Cog):
    def __init__(self, bot: commands.Bot, info):
        self.scheduler = AsyncIOScheduler()
        self.bot = bot
        self.info = info
        self.scheduler.start()
        self.schedule_puzzles()

    async def start_puzzle(self, puzzle_name):
        puzzle = self.info.puzzles[puzzle_name]
        channel = self.bot.get_channel(puzzle.release_channel)
        await channel.send(puzzle.get_text(channel.guild, True))
        for i in range(len(puzzle.image_urls)):
            await channel.send(puzzle.image_urls[i])

    def schedule_puzzles(self):
        for puzzle_name in self.info.puzzles.keys():
            self.schedule_puzzle(puzzle_name)

    def schedule_puzzle(self, puzzle_name):
        puzzle = self.info.puzzles[puzzle_name]
        release_time = datetime.datetime.strptime(puzzle.release_time, self.info.datetime_format)
        if release_time < datetime.datetime.now():
            return
        
        self.scheduler.add_job(self.start_puzzle, "date", run_date=release_time, args=[puzzle_name], id=puzzle_name)

    def reschedule_puzzle(self, puzzle_name):
        try:
            self.scheduler.remove_job(puzzle_name)
        except JobLookupError:
            pass

        self.schedule_puzzle(puzzle_name)
    

async def setup(bot: commands.Bot):
    info = bot.get_cog("Info")
    await bot.add_cog(PuzzleScheduler(bot, info))