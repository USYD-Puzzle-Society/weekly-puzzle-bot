from urllib.parse import _NetlocResultMixinStr
import discord
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
from discord.ext import tasks, commands

TOKEN = "OTk0OTQxODk4NTg4NDM4NTI5.GAo6zJ.lB9k_RyfMIkbhhZrXwJzcW9ZfV-PRzmCYEw5Ik"

command_prefix = "."
bot = commands.Bot(command_prefix=command_prefix)

num_puzzles = 3
puzzle_urls = [None, None, None]

puzz_channel_id = 994948949536407612
puzz_release_datetime = datetime.datetime.now()

ciyk_id = 1002487377958281276

week_count = 1
speed_bonus = 30
puzz_submission_link = "There is no link yet"
jigsaw_emoji = ":jigsaw:"
brain_emoji = ":brain:"
speech_emoji = ":speech_balloon:"
heart_emoji = ":heart:"
cross_emoji = ":x:"

puzz_line1 = f"{jigsaw_emoji} **WEEKLY PUZZLES: WEEK {week_count}**\n\n"
puzz_line2 = f"SPEED BONUS: {speed_bonus} MINUTES\n"
puzz_line3 = f"Hints will be unlimited after {speed_bonus} minutes is up OR after the top 3 solvers have finished!\n\n"
puzz_line4 = f"Submit your answers here: {puzz_submission_link}"
puzz_release_text = puzz_line1 + puzz_line2 + puzz_line3 + puzz_line4

second_best_line1 = f"{brain_emoji} **SECOND BEST: WEEK {week_count}** {brain_emoji}\n\n"
second_best_line2 = f"Try your best to guess what the second most popular answer will be!"
second_best_text = second_best_line1 + second_best_line2

ciyk_line1 = f"{speech_emoji} **COMMENT IF YOU KNOW: WEEK {week_count}** {speech_emoji}\n\n"
ciyk_line2 = f"If you think you know the pattern, comment an answer that follows it in <#{ciyk_id}>\n"
ciyk_line3 = f"We'll react with a {heart_emoji} if you're right and a {cross_emoji} if you're wrong!"
ciyk_text = ciyk_line1 + ciyk_line2 + ciyk_line3

day_names = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}

def format_date(date: datetime.datetime) -> str:
    strdate = date.strftime("%d/%m/%Y")

    return strdate

def format_datetime(date:datetime.datetime) -> str:
    strdatetime = date.strftime("%d/%m/%Y %H:%M")

    return strdatetime

@bot.command()
# assumes rebus is an image
async def setpuzzles(ctx):
    user = ctx.author
    await ctx.send("Please send the puzzles.")
    # only check is for whether the user is the author
    def check(m):
        return m.author == user
    
    is_image = False
    while not is_image:
        msg = await bot.wait_for("message", check=check)

        if msg.attachments:
            is_image = True
            for i in range(num_puzzles):
                puzzle_urls[i] = msg.attachments[i].url

    await ctx.send("Please type the speed bonus for this set of puzzles.")
    
    is_number = False
    while not is_number:
        msg = await bot.wait_for("message", check=check)

    await ctx.send("These are the new puzzles:")
    for i in range(num_puzzles):
        await ctx.send(puzzle_urls[i])

    await ctx.send(
        f"The puzzles are set to release at {puzz_release_datetime}." + 
        "Do `.setpuzztime` if you want to change the release time."
    )

@bot.command()
async def puzzles(ctx):
    await ctx.send(
        "What you see below is exactly what will be released." + 
        f"The puzzles are set to release at {puzz_release_datetime}." + 
        "Do `.setpuzztime` if you want to change the release time."
    )

    await ctx.send(puzz_release_text)
    for i in range(num_puzzles):
        await ctx.send(puzzle_urls[i])

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

@bot.command()
async def test(ctx):
    channel = f"<#{puzz_channel_id}"
    await ctx.send(f"Hi. {channel}>")

@bot.command()
async def start(ctx):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(test, next_run_time=puzz_release_datetime+datetime.timedelta(seconds=1.0))
    scheduler.start()

bot.run(TOKEN)