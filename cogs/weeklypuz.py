import discord
from discord.ext import commands
import os.path
import requests
from info import Info
import json
from json import JSONDecodeError

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

WEEKLYPUZ_FILE = "weeklypuz_name.json"

class WeeklyPuz(commands.Cog):
    def __init__(self, bot, info: Info):
        self.bot = bot
        self.info = info
        self.names: "dict[str, str]" = {}
        try:
            with open(WEEKLYPUZ_FILE, "r") as f:
                self.names = json.load(f)
        except FileNotFoundError:
            open(WEEKLYPUZ_FILE, "x").close()
        except JSONDecodeError:
            pass

    @commands.command()
    async def weeklypuz(self, ctx: commands.context.Context, *args):
        if len(args) < 1 or args[1] not in ["help", "answer", "register"]:
            await ctx.send("Please use the command in the form `.weeklypuz [help/answer/register] ...")
            return
        
        if args[1] == "help":
            pass
        elif args[1] == "answer":
            pass
        elif args[1] == "register":
            self.register(ctx, args[1:])

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

    async def register(self, ctx: commands.context.Context, args: "list[str]"):
        if len(args) < 1:
            await ctx.send("Please register in the form `.weeklypuz register <name>`. Your name can contain multiple words.")
            return
        self.names[ctx.author] = " ".join(args)
        
        try:
            with open(WEEKLYPUZ_FILE, "w") as f:
                json.dump(f)
        except:
            await ctx.send("Something went wrong - contact the developer of this bot.")
            return

        await ctx.send(f"Success! You are now registered as {self.names[ctx.author]}!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != 1100077444922359959:
            return
        await self.bot.get_channel(self.info["rebuscryptic"]["channel_id"]).send("Hints are enabled!")
        
async def setup(bot: commands.Bot):
    info = Info()
    await bot.add_cog(WeeklyPuz(bot, info))
