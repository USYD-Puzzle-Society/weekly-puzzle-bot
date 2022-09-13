import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

class PHC(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.calendar_url = "http://puzzlehuntcalendar.com/"

    def get_events_dict(self) -> dict[str, str]:
        page = requests.get(self.calendar_url)
        soup = BeautifulSoup(page.content, "html.parser")

        events = soup.find_all("div", class_="event")

        """
        stores event in format:
        {
            0: {
                date: '', title = '',
                location: '', description: '',
                link: ''
            }
        }

        0 is a counter and increases for each new event
        """
        events_dict = {}
        for i, event in enumerate(events):
            # get the date, title, location, description and link
            date = event.find("div", class_="date").text
            title = event.find("span", class_="title").text
            location = event.find("span", class_="location").text
            description = event.find("div", class_="description")

            link = description.find("a").text
            only_desc = description.text.replace(f"{link}\n\n", "")

            if location:
                only_desc += f"\n\nLocation: {location}"

            events_dict[i] = {
                "date": date, "title": title,
                "description": only_desc, "link": link
            }
        
        return events_dict

    # def create_embed(self):
    #     events_dict = self.get_events_dict()

    #     embed_msg = discord.Embed(title="Puzzle Hunt Calendar", color=discord.Color.random())

    #     for i in range(len(events_dict)):
    #         event = events_dict[i]

    #         embed_msg.add_field(name=event["date"], value=f"[{event['title']}]({event['link']})", inline=True)
    #         embed_msg.add_field(name="Description", value=event["description"], inline=True)
        
    #     return embed_msg

    # def create_message(self):
    #     events_dict = self.get_events_dict()

    #     text = ""

    #     for i in range(len(events_dict)):
    #         event = events_dict[i]
    #         text += f"**{event['date']}**\n"
    #         text += f"*{event['title']}*\n"
    #         text += event["description"]
        
    #     return text

    def create_embed(self) -> discord.Embed:
        events_dict = self.get_events_dict()

        embed_msg = discord.Embed(title="Puzzle Hunt Calendar", color=discord.Color.random())

        for i in range(len(events_dict)):
            event = events_dict

            embed_msg.add_field(name=f"{i+1}. {event['date']}", value=f"[{event['title']}]({event['link']})")

        return embed_msg
    
    """
    If no arguments are given to the command, then only display the dates and event names in an embed

    If an argument is given, it should be the number of the
    """
    @commands.command(aliases=["puzzhuntcalendar", "phc", "PHC", "puzzhuntcal", "puzzlehuntcal"])
    async def puzzlehuntcalendar(self, ctx: commands.context.Context):
        embed_msg = self.create_embed()

        await ctx.send(embed=embed_msg)

def setup(bot: commands.Bot):
    bot.add_cog(PHC(bot))