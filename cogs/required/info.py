import os
import json
import datetime
import discord
from discord.ext import commands
import classes.puzzle


class Info(commands.Cog):
    def __init__(self):
        self.info_path = "info.json"
        self.load()

    async def check_puzzle_name(self, interaction: discord.Interaction, puzzle_name: str):
        puzzle_aliases = {
            "mon": "monday",
            "wed": "wednesday",
            "fri": "friday",
            "rc": "rebuscryptic"
        }
        puzzle_name = puzzle_name.lower()

        if puzzle_name in puzzle_aliases:
            puzzle_name = puzzle_aliases[puzzle_name]

        if puzzle_name not in self.puzzles:
            accepted_puzzle_names = ', '.join(self.puzzles.keys())
            await interaction.response.send_message(f"Please use one of the accepted puzzle_names: {accepted_puzzle_names}.")
            return False
        
        return puzzle_name

    async def check_time(self, interaction: discord.Interaction, datetime_str: str):
        try:
            _test = datetime.datetime.strptime(datetime_str, self.datetime_format)
            return datetime_str
        except ValueError:
            await interaction.response.send_message(
                "Please enter the date in the format DD/MM/YYYY "
                + "and the time in the format HH:MM (24 hour time)."
            )
            return False

    def next_monday(self, release_time: str) -> str:
        release_time = datetime.datetime.strptime(release_time, self.datetime_format)
        today = datetime.datetime.now()
        days_ahead = 0 - today.weekday() + 7
        next_monday = datetime.datetime.combine(today.date(), release_time.time()) + datetime.timedelta(days=days_ahead)
        return datetime.datetime.strftime(next_monday, self.datetime_format)

    def next_wednesday(self, release_time: str) -> str:
        release_time = datetime.datetime.strptime(release_time, self.datetime_format)
        today = datetime.datetime.now()
        days_ahead = 2 - today.weekday() + 7
        next_wednesday = datetime.datetime.combine(today.date(), release_time.time()) + datetime.timedelta(days=days_ahead)
        return datetime.datetime.strftime(next_wednesday, self.datetime_format)
    
    def next_friday(self, release_time: str) -> str:
        release_time = datetime.datetime.strptime(release_time, self.datetime_format)
        today = datetime.datetime.now()
        days_ahead = 4 - today.weekday() + 7
        next_friday = datetime.datetime.combine(today.date(), release_time.time()) + datetime.timedelta(days=days_ahead)
        return datetime.datetime.strftime(next_friday, self.datetime_format)

    def load(self):
        if os.path.exists(self.info_path):
            with open(self.info_path, "r") as file:
                json_data = json.load(file)
        
        self.datetime_format = json_data["datetime_format"]
        self.day_names = json_data["day_names"]
        self.puzzles = {}

        puzzle_classes = {
            "discussion": classes.puzzle.DiscussionPuzzle,
            "chill": classes.puzzle.ChillPuzzle,
            "weekly": classes.puzzle.WeeklyPuzzle,
            "jff": classes.puzzle.JFFPuzzle
        }

        puzzles = json_data["puzzles"]
        for key in puzzles.keys():
            puzzle_class = puzzle_classes[puzzles[key]["type"]]
            puzzles[key].pop("type")
            puzzle = puzzle_class(**puzzles[key])
            self.puzzles[key] = puzzle

    def save(self):
        puzzle_data = self.puzzles.copy()

        for key in puzzle_data.keys():
            puzzle_data[key] = self.puzzles[key].__dict__
            for puzzle_key in puzzle_data[key].keys():
                if isinstance(puzzle_data[key][puzzle_key], datetime.datetime):
                    puzzle_data[key][puzzle_key] = datetime.datetime.strftime(puzzle_data[key][puzzle_key], self.datetime_format)

        data = {
            "datetime_format": self.datetime_format,
            "day_names": self.day_names,
            "puzzles": puzzle_data
        }

        json_data = json.dumps(data, indent=4)

        with open(self.info_path, "w") as file:
            file.write(json_data)


async def setup(bot: commands.Bot):
    await bot.add_cog(Info())