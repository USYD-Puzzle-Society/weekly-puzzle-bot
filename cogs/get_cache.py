import json
import discord
from discord.ext import tasks, commands

"""
This cog is meant to only be used by me and is not
for public or even admin use.

Some considerations:
- bot.cached_messages only gives the cached messages from the channel the command is called in
    - This might actually be a good thing since not all channels should have messages considered
    - e.g ciyk-discussion mostly doesn't contain useful data
- the bot should automatically save the data every 30 minutes (is 30 minutes too often?)
- should the bot store word counts for different channels separately

"""

USER_ID = 549152699589984256
PUZZSOC_ID = 877860838344634429

class GetCache(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        """
        JSON stores different servers
        Technically this won't really be necessary since the bot is only ever used on
        one server but sometimes it is added into collab hunt servers so this is good for
        separation.

        Format of JSON will be
        {
            server_id: {
                user_object: {
                    top_5_words: ["", "", "", "", ""], # first item in list is most spoken word. "" if no word
                    words: {
                        word: word_count # word count defaults to 0
                    }
                }
            }
        }

        Each time a word has its count increased, check if it's in the top 5 list.
            If so, check if the word should be moved up the list
            If not, check if the word should replace the 5th element in list
        """
        self.msg_count_json = {
            PUZZSOC_ID: {}
        }
    
    @commands.command()
    async def createjson(self, ctx: commands.context.Context):
        pass

    # lists the top five words of the user that called the commands
    @commands.command()
    async def top5(self, ctx: commands.context.Context):
        pass

    # create task that saves the msg_count_json to file every 30 minutes or so