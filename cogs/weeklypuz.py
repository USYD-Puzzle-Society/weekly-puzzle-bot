import discord
from discord.ext import commands
import os.path
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

FORM_API = ""

class WeeklyPuz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        pass

    @commands.command()
    async def weeklypuz(self, ctx: commands.context.Context, *args):
        if len(args) < 1 or args[1] not in ["help", "answer", "setup"]:
            await ctx.send("Please use the command in the form `.weeklypuz [help/answer/setup] ...")
            return
        
        if args[1] == "help":
            pass
        elif args[1] == "answer":
            pass
        elif args[1] == "setup":
            pass

    @commands.command()
    async def answer(self, ctx: commands.context.Context, *args):
        if len(args) < 2:
            await ctx.send("Please submit answer in the form .answer ")
            return

        form_data = {}

        response = requests.post(FORM_API, data=form_data)
        if response.status_code == 200:
            await ctx.send('Form submitted successfully.')
        else:
            await ctx.send('Form submission failed.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != 1100077444922359959:
            return
        await self.bot.get_channel(994948949536407612).send("Hints are enabled!")
        


async def setup(bot: commands.Bot):
    await bot.add_cog(WeeklyPuz(bot))
