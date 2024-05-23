import os
import json
import discord
import datetime
from typing import Callable
from info import Info
from discord.ext import commands


class Setup(commands.Cog):
    def __init__(self, bot: commands.Bot, info: Info):
        self.bot = bot
        self.exec_id = "Executives"
        self.info_obj = info
        self.datetime_format = "%d/%m/%Y %H:%M"

    async def check_puzzle_name(self, ctx: commands.context.Context, puzzle_name: str):
        puzzle_name = self.info_obj.check_puzzle_name(puzzle_name)
        if not puzzle_name:
            accepted_puzzle_names = ', '.join(self.info_obj.default_puzzle_names)
            await ctx.send(f"Please use one of the accepted puzzle_names: {accepted_puzzle_names}")
            return False

        return puzzle_name

    async def check_date(self, ctx: commands.context.Context, date: str):
        date = self.info_obj.check_date(date)
        if not date:
            await ctx.send("Please enter date in the format DD/MM/YYYY")
            return False

        return date

    async def check_time(self, ctx: commands.context.Context, time: str):
        time = self.info_obj.check_time(time)
        if not time:
            await ctx.send("Please enter time in the format HH:MM (24 hour time.)")
            return False
        
        return time

    def new_datetime_and_week(self, original_datetime: str, original_week: int):
        new_datetime = self.info_obj.str_to_datetime(original_datetime)
        new_datetime = new_datetime + datetime.timedelta(days=7)
        new_datetime = new_datetime.strftime(self.datetime_format)

        return (new_datetime, original_week + 1)

    async def get_image_urls(self, ctx: commands.context.Context, message_from_author: Callable):
        await ctx.send(
            "Please send all the images for the puzzle in one message."
            + " Type `.stop` at any time and no changes will be made."
        )

        msg = await self.bot.wait_for("message", check=message_from_author)

        if ".stop" == msg.content.lower():
            await ctx.send("Command stopped. No changes have been made.")
            return []

        while not len(msg.attachments):
            await ctx.send(
                "Please send all the images for the puzzle in one message."
                + " Type `.stop` at any time and no changes will be made."
            )

            msg = await self.bot.wait_for("message", check=message_from_author)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made.")
                return []

        return [image.url for image in msg.attachments]

    async def get_submission_link(self, ctx: commands.context.Context, message_from_author: Callable):
        await ctx.send("Please send the submission link.")

        msg = await self.bot.wait_for("message", check=message_from_author)

        if ".stop" == msg.content.lower():
            await ctx.send("Command stopped. No changes have been made.")
            return ""

        return msg.content

    async def get_interactive_link(self, ctx: commands.context.Context, message_from_author: Callable):
        await ctx.send("Is there an interactive link? y/n")

        msg = await self.bot.wait_for("message", check=message_from_author)

        if ".stop" == msg.content.lower():
            await ctx.send("Command stopped. No changes have been made.")
            return ""

        while not msg.content.lower() == "y":
            if "n" == msg.content.lower():
                return ""

            await ctx.send("Is there an interactive link? y/n")

            msg = await self.bot.wait_for("message", check=message_from_author)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made.")
                return ""
            
        await ctx.send("Please send the interactive link for the puzzle.")

        msg = await self.bot.wait_for("message", check=message_from_author)

        if ".stop" == msg.content.lower():
            await ctx.send("Command stopped. No changes have been made.")
            return ""

        return msg.content

    async def get_date(self, ctx: commands.context.Context, message_from_author: Callable):
        await ctx.send(
            "Please enter the new release date for the rebus and cryptic in the format DD/MM/YYYY."
            + "Do `.stop` at any time to exit and no changes will be made."
        )
        
        msg = await self.bot.wait_for("message", check=message_from_author)

        if ".stop" == msg.content.lower():
            await ctx.send("Command stopped. No changes have been made.")
            return

        date = await self.check_date(msg.content)
        
        while not date:
            msg = await self.bot.wait_for("message", check=message_from_author)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made.")
                return

            date = await self.check_date(msg.content)
            
        return date

    async def get_time(self, ctx: commands.context.Context, message_from_author: Callable):
        await ctx.send(
            "Please enter the new release time for the puzzles in the format HH:MM (24 hour time)."
            + "Do `.stop` at any time to exit and no changes will be made."
        )

        msg = await self.bot.wait_for("message", check=check)

        if ".stop" == msg.content.lower():
            await ctx.send("Command stopped. No changes have been made.")
            return

        time = self.info_obj.check_is_time(msg.content)

        while not time:
            await ctx.send("Please enter time in the format HH:MM (24 hour time.)")
            
            msg = await self.bot.wait_for("message", check=message_from_author)

            if ".stop" == msg.content.lower():
                await ctx.send("Command stopped. No changes have been made.")
                return

            time = self.info_obj.check_is_time(msg.content)
            
        return time

    async def set_time(self, ctx: commands.context.Context, puzzle_name: str):
        def message_from_author(msg):
            return msg.author == ctx.author

        await ctx.send(
            "The current release time for the puzzle is "
            + f"{self.info_obj.info[puzzle_name]['release_datetime']}"
        )
        
        year, month, day = self.get_date(ctx, message_from_author)
        release_date = datetime.date(year, month, day)
        weekday_name = self.info_obj.day_names[release_date.weekday()]

        await ctx.send(
            f"The new release date is now {release_date.strftime('%d/%m/%Y')} ({weekday_name})"
        )

        hour, minute = self.get_time(ctx, message_from_author)
        
        new_release = datetime.datetime(year, month, day, hour, minute)
        self.info_obj.change_time(puzzle_name, new_release)

        await ctx.send(
            f"The new release time for the puzzle is {new_release.strftime(self.info_obj.datetime_format)} ({weekday_name}). "
            + "Remember to do `.start rc`"
        )

    # command for quick setup of puzzles. user will only have to send the images
    @commands.command()
    @commands.has_role("Executives")
    async def qset(
            self, ctx: commands.context.Context, puzzle_name: str, 
            change_datetime: str = "true"):
        def message_from_author(msg):
            return msg.author == ctx.author

        puzzle_name = await self.check_puzzle_name(ctx, puzzle_name)
        if not puzzle_name:
            return

        original_data = self.info_obj.info[puzzle_name]

        if change_datetime == "true":
            release_datetime, week_num = self.new_datetime_and_week(
                original_data["release_datetime"], 
                original_data["week_num"]
            )
        else:
            release_datetime = original_data["release_datetime"]
            week_num = original_data["week_num"]

        img_urls = await self.get_image_urls(ctx, message_from_author)
        if img_urls == []:
            return

        submission_link = await self.get_submission_link(ctx, message_from_author)
        if submission_link == "":
            return

        interactive_link = await self.get_interactive_link(ctx, message_from_author)
        
        puzzle_data = {
            "release_datetime": release_datetime,
            "week_num": week_num,
            "img_urls": img_urls,
            "submission_link": submission_link,
            "interactive_link": interactive_link,
        }

        self.info_obj.change_data(puzzle_name, puzzle_data)
        
        await ctx.send(
            f"Done. The following will be released at {release_datetime} in <#{original_data['channel_id']}>. "
            + f"Remember to do `.start {puzzle_name}`"
        )

        text = self.info_obj.get_text(ctx, False, puzzle_name)
        await ctx.send(text)
        for i in range(len(img_urls)):
            await ctx.send(img_urls[i])

    @commands.command()
    @commands.has_role("Executives")
    async def qsettime(
            self, ctx: commands.context.Context, puzzle_name: str, date: str, 
            time: str):
        puzzle_name = await self.check_puzzle_name(ctx, puzzle_name)
        if not puzzle_name:
            return

        new_date = await self.check_date(ctx, date)
        if not new_date:
            return
        day, month, year = new_date

        release_date = datetime.date(year, month, day)
        weekday_name = self.info_obj.day_names[release_date.weekday()]

        new_time = await self.check_time(ctx, time)
        if not new_time:
            return
        hour, minute = new_time

        new_release = datetime.datetime(year, month, day, hour, minute)
        self.info_obj.change_time(puzzle_name, new_release)

        await ctx.send(
            f"The new release time for the puzzles is "
            + f"{new_release.strftime(self.info_obj.datetime_format)} ({weekday_name}). "
            + f"Remember to do `.start {puzzle_name}`"
        )

    @commands.command()
    @commands.has_role("Executives")
    async def qsetweek(
            self, ctx: commands.context.Context, puzzle_name: str,
            week_num: str):
        puzzle_name = await self.check_puzzle_name(ctx, puzzle_name)
        if not puzzle_name:
            return

        # this will be removed with slash commands
        try:
            new_week = int(week_num)
        except ValueError:
            await ctx.send("Please enter the week as a number.")
            return

        self.info_obj.change_week(puzzle_name, new_week)

        await ctx.send(
            f"The new week number for the {puzzle_name.capitalize()} puzzle is "
            + f"{self.info_obj.info[puzzle_name]['week_num']}. "
            + f"Remember to do `.start {puzzle_name}`"
        )

    @commands.command()
    @commands.has_role("Executives")
    async def setrctime(self, ctx: commands.context.Context):
        await self.set_time(ctx, "rebuscryptic")

    """
    Thinking of making it so that this command allows the user to
    put the release date and time in the command call.
    Like: `.setminipuzztime 12/08/2022 11:00`
    """

    @commands.command()
    @commands.has_role("Executives")
    async def setminipuzztime(self, ctx: commands.context.Context):
        await self.set_time(ctx, "minipuzzle")

    @commands.command()
    @commands.has_role("Executives")
    async def setcrosswordtime(self, ctx: commands.context.Context):
        await self.set_time(ctx, "crossword")

    @commands.command()
    @commands.has_role("Executives")
    async def setwordsearchtime(self, ctx: commands.context.Context):
        await self.set_time(ctx, "wordsearch")

    @commands.command()
    @commands.has_role("Executives")
    async def setlogicpuzztime(self, ctx: commands.context.Context):
        await self.set_time(ctx, "logicpuzz")

    @commands.command()
    @commands.has_role("Executives")
    async def setciyktime(self, ctx: commands.context.Context):
        await self.set_time(ctx, "ciyk")

    @commands.command()
    @commands.has_role("Executives")
    async def setrc(self, ctx: commands.context.Context):
        await self.qset(ctx, "rebuscryptic")

    @commands.command()
    @commands.has_role("Executives")
    async def setminipuzz(self, ctx: commands.context.Context):
        await self.qset(ctx, "minipuzz")

    @commands.command()
    @commands.has_role("Executives")
    async def setcrossword(self, ctx: commands.context.Context):
        await self.qset(ctx, "crossword")

    @commands.command()
    @commands.has_role("Executives")
    async def setwordsearch(self, ctx: commands.context.Context):
        await self.qset(ctx, "wordsearch")

    @commands.command()
    @commands.has_role("Executives")
    async def setlogicpuzz(self, ctx: commands.context.Context):
        self.qset(ctx, "logicpuzz")

    @commands.command()
    @commands.has_role("Executives")
    async def setciyk(self, ctx: commands.context.Context):
        self.qset(ctx, "ciyk")


async def setup(bot: commands.Bot):
    info = Info()
    await bot.add_cog(Setup(bot, info))
