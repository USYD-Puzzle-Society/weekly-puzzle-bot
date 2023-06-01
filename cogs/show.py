import os
import json
import discord
import datetime
from info import Info
from discord.ext import commands

class Show(commands.Cog):
    def __init__(self, bot: commands.Bot, info: Info):
        self.bot = bot

        self.info_obj = info
    
    """
    Fix to have only one method
    """

    @commands.command()
    @commands.has_role("Executives")
    async def showrc(self, ctx: commands.context.Context):
        rc_info = self.info_obj.info["rebuscryptic"]
        rc_text = self.info_obj.get_rebuscryptic_text(ctx, False)
        rc_time = rc_info["release_datetime"]
        rc_channel = rc_info["channel_id"]

        await ctx.send(f"The following will be released at {rc_time} in <#{rc_channel}>")
        await ctx.send(rc_text)
        for i in range(len(rc_info["img_urls"])):
            await ctx.send(rc_info["img_urls"][i])

    @commands.command()
    @commands.has_role("Executives")
    async def showminipuzz(self, ctx: commands.context.Context):
        puzz_info = self.info_obj.info["minipuzz"]
        puzz_text = self.info_obj.get_minipuzz_text(ctx, False)
        puzz_time = puzz_info["release_datetime"]
        puzz_channel = puzz_info["channel_id"]

        await ctx.send(f"The following will be released at {puzz_time} in <#{puzz_channel}>.")
        await ctx.send(puzz_text)
        for i in range(len(puzz_info["img_urls"])):
            await ctx.send(puzz_info["img_urls"][i])

    @commands.command()
    @commands.has_role("Executives")
    async def showcrossword(self, ctx: commands.context.Context):
        crossword_info = self.info_obj.info["crossword"]
        crossword_text = self.info_obj.get_rebuscryptic_text(ctx, False)
        crossword_time = crossword_info["release_datetime"]
        crossword_channel = crossword_info["channel_id"]

        await ctx.send(f"The following will be released at {crossword_time} in <#{crossword_channel}>")
        await ctx.send(crossword_text)
        for i in range(len(crossword_info["img_urls"])):
            await ctx.send(crossword_info["img_urls"][i])

    @commands.command()
    @commands.has_role("Executives")
    async def showsudoku(self, ctx: commands.context.Context):
        sudoku_info = self.info_obj.info["sudoku"]
        sudoku_text = self.info_obj.get_rebuscryptic_text(ctx, False)
        sudoku_time = sudoku_info["release_datetime"]
        sudoku_channel = sudoku_info["channel_id"]

        await ctx.send(f"The following will be released at {sudoku_time} in <#{sudoku_channel}>")
        await ctx.send(sudoku_text)
        for i in range(len(sudoku_info["img_urls"])):
            await ctx.send(sudoku_info["img_urls"][i])

    @commands.command()
    @commands.has_role("Executives")
    async def showciyk(self, ctx: commands.context.Context):
        ciyk_info = self.info_obj.info["ciyk"]
        ciyk_text = self.info_obj.get_ciyk_text(ctx, False)
        ciyk_time = ciyk_info["release_datetime"]
        ciyk_channel = ciyk_info["channel_id"]

        await ctx.send(f"The following will be set at {ciyk_time} in <#{ciyk_channel}>.")
        await ctx.send(ciyk_text)
        for i in range(len(ciyk_info["img_urls"])):
            await ctx.send(ciyk_info["img_urls"][i])

async def setup(bot: commands.Bot):
    info = Info()
    await bot.add_cog(Show(bot, info))