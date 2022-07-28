import discord
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
from discord.ext import tasks, commands

TOKEN = "OTk0OTQxODk4NTg4NDM4NTI5.GAo6zJ.lB9k_RyfMIkbhhZrXwJzcW9ZfV-PRzmCYEw5Ik"

command_prefix = "."
bot = commands.Bot(command_prefix=command_prefix)

puzzle_urls = {
    "rebus": None,
    "cryptic": None,
    "minipuzzz": None
}

day_names = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}

puzz_channel_id = 994948949536407612
puzz_release_datetime = datetime.datetime.now()

def format_date(date: datetime.datetime) -> str:
    strdate = date.strftime("%d/%m/%Y")

    return strdate

def format_datetime(date:datetime.datetime) -> str:
    strdatetime = date.strftime("%d/%m/%Y %H:%M")

    return strdatetime

@bot.command()
# assumes rebus is an image
async def setrebus(ctx):
    user = ctx.author
    await ctx.send(f"The current rebus is: {puzzle_urls['rebus']} \nPlease send the image of the new rebus.")

    # only check is for whether the user is the author
    def check(m):
        return m.author == user
    
    is_image = False
    while not is_image:
        msg = await bot.wait_for("message", check=check)

        if msg.attachments:
            is_image = True
            puzzle_urls["rebus"] = msg.attachments[0].url

    await ctx.send(f"The rebus is now:")
    await ctx.send(puzzle_urls["rebus"])

@bot.command()
async def rebus(ctx):
    if not puzzle_urls["rebus"]:
        await ctx.send("The current rebus is: None")
    else:
        await ctx.send("The current rebus is:")
        await ctx.send(puzzle_urls["rebus"])

@bot.command()
async def bird(ctx):
    with open("b03.jpeg", "rb") as b:
        bird = discord.File(b)
        await ctx.send(file=bird)

@bot.command()
async def puzztime(ctx):
    puzz_time = format_datetime(puzz_release_datetime)
    await ctx.send(f"The current puzzle release time is {puzz_time}.")

@bot.command()
async def setpuzztime(ctx):
    user = ctx.author
    
    global puzz_release_datetime
    puzz_time = format_datetime(puzz_release_datetime)
    await ctx.send(f"The current puzzle release time is {puzz_time}.")

    await ctx.send("Please enter the new release date of the puzzles in the format DD/MM/YYYY.")
    # only check is for whether the user is the author
    def check(m):
        return m.author == user

    # get the new desired release date from user
    valid_date = False
    while not valid_date:
        msg = await bot.wait_for("message", check=check)

        try:
            strday, strmonth, stryear = msg.content.split("/")

            # check if it is a valid date
            date = datetime.date(int(stryear), int(strmonth), int(strday))

            day, month, year = int(strday), int(strmonth), int(stryear)

            valid_date = True
        
        except ValueError:
            await ctx.send(f"{msg.content} is not a valid date. Please try again.")

    new_puzz_date = format_date(date)
    puzzle_day = day_names[date.weekday()]
    await ctx.send(f"The new puzzle release date is now {new_puzz_date} ({puzzle_day}).")
    await ctx.send("Please enter the new release time of the puzzles in the format HH:MM (24 hour time).")

    valid_time = False
    while not valid_time:
        msg = await bot.wait_for("message", check=check)

        try:
            strhour, strminute = msg.content.split(":")

            # check if valid time
            date = datetime.time(int(strhour), int(strminute))

            hour, minute = int(strhour), int(strminute)

            valid_time = True
        
        except ValueError:
            await ctx.send(f"{msg.content} is not a valid time. Please try again.")

    puzz_release_datetime = datetime.datetime(year, month, day, hour, minute)

    await ctx.send(f"The new puzzle release time is now {format_datetime(puzz_release_datetime)} ({puzzle_day}).")

async def test():
    puzz_channel = bot.get_channel(puzz_channel_id)
    await puzz_channel.send(f"This is a message that was scheduled for {format_datetime(puzz_release_datetime)}.")

@bot.command()
async def start(ctx):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(test, next_run_time=puzz_release_datetime+datetime.timedelta(seconds=1.0))
    scheduler.start()

bot.run(TOKEN)