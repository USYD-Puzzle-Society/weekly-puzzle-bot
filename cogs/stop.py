import json
from info import Info
from discord.ext import commands

class Stop(commands.Cog):
    def __init__(self, bot: commands.Bot, info: Info):
        self.bot = bot
        self.info_obj = info
        self.start_json = "start.json"

    @commands.command()
    async def stop(self, ctx, release_id):
        with open(self.start_json, "r") as sj:
            currently_releasing = json.load(sj)
        
        try:
            release = currently_releasing[release_id]
            release_text = release["text"]
            release_urls = None
            
            if "urls" in release:
                release_urls = release["urls"]

            release_datetime = release["datetime"]
            release_channel = release["channel"]
             
            del currently_releasing[release_id]
            new_json = json.dumps(currently_releasing, indent=4)

            with open(self.start_json, "w") as sj:
                sj.write(new_json)

            await ctx.send(f"Done. The below will no longer release at {release_datetime} in <#{release_channel}>.")
            await ctx.send(release_text)
            if release_urls:
                for i in range(len(release_urls)):
                    await ctx.send(release_urls[i])

        except KeyError as ke:
            print(ke)
            await ctx.send(f"There is no announcement release with the ID {release_id}")

async def setup(bot: commands.Bot):
    info = Info()
    await bot.add_cog(Stop(bot, info))