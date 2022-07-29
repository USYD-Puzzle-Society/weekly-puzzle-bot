from urllib.parse import _NetlocResultMixinStr
import discord
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
from discord.ext import tasks, commands
from Puzzles import Puzzles

TOKEN = "OTk0OTQxODk4NTg4NDM4NTI5.GAo6zJ.lB9k_RyfMIkbhhZrXwJzcW9ZfV-PRzmCYEw5Ik"

command_prefix = "."
bot = commands.Bot(command_prefix=command_prefix)

num_puzzles = 2

ciyk_id = 1002487377958281276

puzzles = Puzzles(num_puzzles)

setting_puzzles = {}

week_count = 1
jigsaw_emoji = ":jigsaw:"
brain_emoji = ":brain:"
speech_emoji = ":speech_balloon:"
heart_emoji = ":heart:"
cross_emoji = ":x:"

def get_puzz_text(puzzles: Puzzles):
    puzz_line1 = f"{jigsaw_emoji} **WEEKLY PUZZLES: WEEK {week_count}**{jigsaw_emoji}\n\n"
    puzz_line2 = f"SPEED BONUS: {puzzles.speed_bonus} MINUTES\n"
    puzz_line3 = f"Hints will be unlimited after {puzzles.speed_bonus} minutes is up OR after the top 3 solvers have finished!\n\n"
    puzz_line4 = f"Submit your answers here: {puzzles.submission_link}"
    
    puzz_release_text = puzz_line1 + puzz_line2 + puzz_line3 + puzz_line4
    return puzz_release_text

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

def check_setting_puzzles(user):
    try:
        return setting_puzzles[user]
    except KeyError:
        return False

@bot.command()
async def setpuzzchannel(ctx):
    user = ctx.author
    channel_id = puzzles.channel_id
    text = ""
    if -1 == channel_id:
        text += "No channel has been selected yet. "
    else:
        text += f"The current channel is <#{puzzles.channel_id}>. "

    text += "Please enter the ID of the new channel where you would like the puzzles to be released."
    text += "If you don't know how to get the ID of a channel, simply right click the channel and then click \"Copy ID\""

    await ctx.send(text)

    def check(m):
        return m.author == user

    msg = await bot.wait_for("message", check=check)

    # check if number
    try:
        new_id = int(msg.content)

        # check if valid channel id
        new_channel = bot.get_channel(new_id)

        if not new_channel:
            await ctx.send(f"{new_id} is not a valid channel id.")
        else:
            puzzles.change_channel_id(new_id)

            await ctx.send(f"The puzzles will now be released in <#{puzzles.channel_id}>")
    
    except ValueError:
        await ctx.send(f"{msg.content} is not a valid channel id.")

@bot.command()
async def setpuzzles(ctx):
    user = ctx.author
    is_setting_puzzles = check_setting_puzzles(user)
    if is_setting_puzzles:
        await ctx.send("You are already using this command.")
        return

    # first check if a channel has been set for the puzzles to release in
    channel_id = puzzles.channel_id
    if -1 == channel_id:
        await ctx.send("No channel has been set for the puzzles. Please first change this by using `.setpuzzchannel`.")
        return
    else:
        # check if valid channel
        channel = bot.get_channel(channel_id)

        if not channel:
            await ctx.send("The channel for the puzzles no longer exists. Please first change the channel by using `.setpuzzchannel`.")
            return

    setting_puzzles[user] = True
    await ctx.send("Please send the puzzle images in a single message.")
    # only check is for whether the user is the author
    def check(m):
        return m.author == user
    
    # get the puzzle images
    is_image = False
    while not is_image:
        msg = await bot.wait_for("message", check=check)

        if len(msg.attachments) == num_puzzles:
            is_image = True
            puzzles.change_puzzles(msg.attachments)
        else:
            await ctx.send(f"Please send all {num_puzzles} puzzle images in a single message.")


    await ctx.send("Please enter the speed bonus for this set of puzzles.")
    # get the speed bonus
    is_number = False
    while not is_number:
        msg = await bot.wait_for("message", check=check)

        try:
            bonus = int(msg.content)
            is_number = True

            puzzles.change_bonus(bonus)

        except ValueError:
            await ctx.send("Please type a number.")

    # get the submission link
    await ctx.send("Please send the submission link for the puzzles.")
    msg = await bot.wait_for("message", check=check)
    puzzles.change_link(msg.content)

    setting_puzzles[user] = False

    await ctx.send(
        f"The below is what will be released at {puzzles.release_datetime} in <#{puzzles.channel_id}>." +
        "Do `.setpuzztime` if you want to change the release time or `.setpuzzchannel` if" + 
        "you want to change the channel the puzzles are released in."
    )

    puzz_text = get_puzz_text(puzzles)
    await ctx.send(puzz_text)
    for i in range(num_puzzles):
        await ctx.send(puzzles.urls[i])

@bot.command()
async def showpuzzles(ctx):
    # check if any puzzles have been set
    if None in puzzles.urls:
        await ctx.send("The puzzles have not been assigned, yet. Please do so by using `.setpuzzles`.")
        return

    await ctx.send(
        f"The below is what will be released at {puzzles.release_datetime} in <#{puzzles.channel_id}>." +
        "Do `.setpuzztime` if you want to change the release time or `.setpuzzchannel` if" + 
        "you want to change the channel the puzzles are released in."
    )

    puzz_text = get_puzz_text(puzzles)
    await ctx.send(puzz_text)
    for i in range(num_puzzles):
        await ctx.send(puzzles.urls[i])

@bot.command()
async def bird(ctx):
    with open("b03.jpeg", "rb") as b:
        bird = discord.File(b)
        await ctx.send(file=bird)

@bot.command()
async def puzztime(ctx):
    puzz_time = format_datetime(puzzles.release_datetime)
    await ctx.send(f"The current puzzle release time is {puzz_time}.")

@bot.command()
async def setpuzztime(ctx):
    user = ctx.author
    
    puzz_time = format_datetime(puzzles.release_datetime)
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

    puzzles.release_datetime = datetime.datetime(year, month, day, hour, minute)

    await ctx.send(f"The new puzzle release time is now {format_datetime(puzzles.release_datetime)} ({puzzle_day}).")

@bot.command()
async def test(ctx):
    channel = f"<#{puzzles.channel_id}"
    await ctx.send(f"Hi. {channel}>")

@bot.command()
async def start(ctx):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(test, next_run_time=puzzles.release_datetime + datetime.timedelta(seconds=1.0))
    scheduler.start()

bot.run(TOKEN)