import discord
from discord.ext import commands
import os.path
import requests
from info import Info
import json
from json import JSONDecodeError
import re

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
    async def answer(self, ctx: commands.context.Context, args: "list[str]"):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send("Please DM the bot with this command!")
            return

        if len(args) < 2 or args[0] not in ["rc", "minipuz"]:
            await ctx.send("Please submit answer in the form .answer [rc/minipuz] <answer>")
            return
    
        if ctx.author.id not in self.names:
            await ctx.send("You're not yet registered - use the command `.weeklypuz register` to register.")
            return
        
        form_data = {}
        
        if args[0] == "rc":
            match = re.fullmatch(r"https://docs\.google\.com/forms/d/e/(.+?)/viewform\?usp=pp_url&(entry\.\d+)=a&(entry\.\d+)=a&(entry\.\d+)=a&(entry\.\d+)=a",  
                                 self.info["rebuscryptic"]["prefilled_submission_link"])
            form_id = match.group(1)
            form_data = {
                match.group(2): ctx.author.id,
                match.group(3): self.names[ctx.author.id],
                match.group(4): args[0],
                match.group(5): args[1]
            }
        
        elif args[0] == "minipuz":
            match = re.fullmatch(r"https://docs\.google\.com/forms/d/e/(.+?)/viewform\?usp=pp_url&(entry\.\d+)=a&(entry\.\d+)=a&(entry\.\d+)=a",
                                self.info["minipuz"]["prefilled_submission_link"])
            form_id = match.group(1)
            form_data = {
                match.group(2): ctx.author.id,
                match.group(3): self.names[ctx.author.id],
                match.group(4): args[0]
            }

        form_api = f"https://docs.google.com/forms/u/0/d/e/{form_id}/formResponse"

        response = requests.post(form_api, data=form_data)
        if response.status_code == 200:
            await ctx.send('Form submitted successfully.')
        else:
            await ctx.send('Form submission failed.')

    async def register(self, ctx: commands.context.Context, args: "list[str]"):
        if len(args) < 1:
            await ctx.send("Please register in the form `.weeklypuz register <name>`. Your name can contain multiple words.")
            return
        self.names[ctx.author.id] = " ".join(args)
        
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
