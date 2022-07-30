import discord
import asyncio
import datetime
from discord.ext import commands
from Puzzles import Puzzles
from SecondBest import SecondBest
from CIYK import CIYK

TOKEN = "OTk0OTQxODk4NTg4NDM4NTI5.GAo6zJ.lB9k_RyfMIkbhhZrXwJzcW9ZfV-PRzmCYEw5Ik"

command_prefix = "."
bot = commands.Bot(command_prefix=command_prefix)

num_puzzles = 2

puzzles = Puzzles(num_puzzles, datetime.datetime.now())
sb = SecondBest(datetime.datetime.now())
ciyk = CIYK(datetime.datetime.now())

setting_puzzles = {}

week_count = 1
jigsaw_emoji = ":jigsaw:"
brain_emoji = ":brain:"
speech_emoji = ":speech_balloon:"
heart_emoji = ":heart:"
cross_emoji = ":x:"


def get_puzz_text(ctx, puzzles: Puzzles):
    puzz_mention = f"{discord.utils.get(ctx.guild.roles, id=puzzles.role_id).mention}\n\n"
    puzz_line1 = f"{jigsaw_emoji} **WEEKLY PUZZLES: WEEK {puzzles.week_count}** {jigsaw_emoji}\n\n"
    puzz_line2 = f"**SPEED BONUS:** {puzzles.speed_bonus} MINUTES\n"
    puzz_line3 = f"*Hints will be unlimited after {puzzles.speed_bonus} minutes is up OR after the top 3 solvers have finished!*\n\n"
    puzz_line4 = f"**Submit your answers here:** {puzzles.submission_link}\n"
    puzz_line5 = "You can submit as many times as you want!\n"
    puzz_line6 = "Your highest score will be kept."
    
    puzz_release_text = puzz_mention + puzz_line1 + puzz_line2 + puzz_line3 + puzz_line4 + puzz_line5 + puzz_line6
    return puzz_release_text

def get_sb_text(ctx, sb: SecondBest):
    sb_mention = f"{discord.utils.get(ctx.guild.roles, id=sb.role_id).mention}\n\n"
    second_best_line1 = f"{brain_emoji} **SECOND BEST: WEEK {sb.week_count}** {brain_emoji}\n\n"
    second_best_line2 = f"Try your best to guess what the second most popular answer will be!\n\n"
    second_best_line3 = f"**Submit your answer here:** {sb.submission_link}\n\n"

    second_best_text = sb_mention + second_best_line1 + second_best_line2 + second_best_line3 + sb.img_url
    return second_best_text

def get_ciyk_text(ctx, ciyk: CIYK):
    ciyk_mention = f"{discord.utils.get(ctx.guild.roles, id=ciyk.role_id).mention}\n\n"
    ciyk_line1 = f"{speech_emoji} **COMMENT IF YOU KNOW: WEEK {ciyk.week_count}** {speech_emoji}\n\n"
    ciyk_line2 = f"If you think you know the pattern, comment an answer that follows it in <#{ciyk.discuss_id}>\n"
    ciyk_line3 = f"We'll react with a {heart_emoji} if you're right and a {cross_emoji} if you're wrong!\n\n"

    ciyk_text = ciyk_mention + ciyk_line1 + ciyk_line2 + ciyk_line3 + ciyk.img_url
    return ciyk_text

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
        f"The below is what will be released at {format_datetime(puzzles.release_datetime)} in <#{puzzles.channel_id}>." +
        "Do `.setpuzztime` if you want to change the release time or `.setpuzzchannel` if " + 
        "you want to change the channel the puzzles are released in.\n" + 
        "Remember to do `.startpuzz`"
    )

    puzz_text = get_puzz_text(ctx, puzzles)
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
        f"The below is what will be released at {puzzles.release_datetime} in <#{puzzles.channel_id}>. " +
        "Do `.setpuzztime` if you want to change the release time or `.setpuzzchannel` if" + 
        "you want to change the channel the puzzles are released in.\n" + 
        "Remember to do `.startpuzz`"
    )

    puzz_text = get_puzz_text(ctx, puzzles)
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

def check_is_date(msg: str):
    try:
        strday, strmonth, stryear = msg.content.split("/")

        # check if it is a valid date
        date = datetime.date(int(stryear), int(strmonth), int(strday))

        day, month, year = int(strday), int(strmonth), int(stryear)

        return day, month, year
    
    except ValueError:
        return False

def check_is_time(msg: str):
    try:
        strhour, strminute = msg.content.split(":")

        # check if valid time
        time = datetime.time(int(strhour), int(strminute))

        hour, minute = int(strhour), int(strminute)

        return hour, minute

    except ValueError:
        return False

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

        date = check_is_date(msg)
        if not date:
            await ctx.send(f"\"{msg.content}\" is not a valid date. Please try again.")
        else:
            day, month, year = date
            valid_date = True

    new_puzz_date = format_date(datetime.datetime(year, month, day))
    puzzle_day = day_names[datetime.datetime(year, month, day).weekday()]
    await ctx.send(f"The new puzzle release date is now {new_puzz_date} ({puzzle_day}).")
    await ctx.send("Please enter the new release time of the puzzles in the format HH:MM (24 hour time).")

    valid_time = False
    while not valid_time:
        msg = await bot.wait_for("message", check=check)

        time = check_is_time(msg)

        if not time:
            await ctx.send(f"\"{msg.content}\" is not a valid time. Please try again.")
        else:
            hour, minute = time
            valid_time = True

    puzzles.release_datetime = datetime.datetime(year, month, day, hour, minute)

    await ctx.send(
        f"The new puzzle release time is now {format_datetime(puzzles.release_datetime)} ({puzzle_day}). " + 
        "Remember to do `.startpuzz`"
    )

@bot.command()
async def setsb(ctx):
    user = ctx.author
    await ctx.send("Please send the image for the Second Best game.")

    def check(m):
        return m.author == user
    
    valid_image = False
    while not valid_image:
        msg = await bot.wait_for("message", check=check)

        if not msg.attachments:
            await ctx.send("Please send the image for the Second Best game.")
        else:
            sb.change_url(msg.attachments[0].url)
            valid_image = True

    
    await ctx.send("Please send the submission link for Second Best.")

    msg = await bot.wait_for("message", check=check)
    sb.change_link(msg.content)

    await ctx.send(
        f"Below is what will be released at {format_datetime(sb.release_datetime)} in <#{sb.channel_id}>. " + 
        "Remember to do `.startsb`"
    )

    sb_text = get_sb_text(ctx, sb)
    await ctx.send(sb_text)

@bot.command()
async def setsbtime(ctx):
    user = ctx.author

    def check(m):
        return m.author == user
    
    sb_time = format_datetime(sb.release_datetime)
    await ctx.send(f"The current Second Best release time is {sb_time}.")

    await ctx.send("Please enter the new release date of Second Best in the format DD/MM/YYYY.")

    while True:
        msg = await bot.wait_for("message", check=check)

        date = check_is_date(msg)

        if not date:
            await ctx.send(f"\"{msg.content}\" is not a valid date. Please try again.")
        else:
            day, month, year = date
            break

    day_name = day_names[datetime.date(year, month, day).weekday()]
    await ctx.send(f"Release date now set for: {datetime.date(year, month, day)} ({day_name}).")
    await ctx.send("Please enter the new release time of Second Best in the format HH:MM (24 hour time).")

    while True:
        msg = await bot.wait_for("message", check=check)

        time = check_is_time(msg)

        if not time:
            await ctx.send(f"\"{msg.content}\" is not a valid time. Please try again.")
        else:
            hour, minute = time
            break
    
    sb.release_datetime = datetime.datetime(year, month, day, hour, minute)
    await ctx.send(
        f"The new Second Best release time is now {format_datetime(sb.release_datetime)}. " + 
        "Remember to do `.startsb`"
    )

@bot.command()
async def showsb(ctx):
    sb_text = get_sb_text(ctx, sb)

    await ctx.send(
        f"Below is what will be released at {format_datetime(sb.release_datetime)} in <#{sb.channel_id}>. " + 
        "Remember to do `.startsb`"
    )

    await ctx.send(sb_text)

@bot.command()
async def setciyk(ctx):
    user = ctx.author
    await ctx.send("Please send the image for the CIYK.")

    def check(m):
        return m.author == user

    valid_image = False
    while not valid_image:
        msg = await bot.wait_for("message", check=check)

        if not msg.attachments:
            await ctx.send("Please send the image for the CIYK.")
        else:
            ciyk.change_url(msg.attachments[0].url)
            valid_image = True
    
    await ctx.send(
        f"Below is what will be released at {format_datetime(ciyk.release_datetime)} in <#{ciyk.channel_id}>. " +
        "Remember to do `.startciyk`"
    )

    ciyk_text = get_ciyk_text(ctx, ciyk)
    await ctx.send(ciyk_text)

@bot.command()
async def setciyktime(ctx):
    user = ctx.author

    def check(m):
        return m.author == user
    
    ciyk_time = format_datetime(ciyk.release_datetime)
    await ctx.send(f"The current CIYK release time is {ciyk_time}.")

    await ctx.send("Please enter the new release date of CIYK in the format DD/MM/YYYY.")

    while True:
        msg = await bot.wait_for("message", check=check)

        date = check_is_date(msg)

        if not date:
            await ctx.send(f"\"{msg.content}\" is not a valid date. Please try again.")
        else:
            day, month, year = date
            break

    day_name = day_names[datetime.date(year, month, day).weekday()]
    await ctx.send(f"Release date now set for: {datetime.date(year, month, day)} ({day_name}).")
    await ctx.send("Please enter the new release time of CIYK in the format HH:MM (24 hour time).")

    while True:
        msg = await bot.wait_for("message", check=check)

        time = check_is_time(msg)

        if not time:
            await ctx.send(f"\"{msg.content}\" is not a valid time. Please try again.")
        else:
            hour, minute = time
            break
    
    ciyk.release_datetime = datetime.datetime(year, month, day, hour, minute)
    await ctx.send(
        f"The new CIYK release time is now {format_datetime(ciyk.release_datetime)}. " + 
        "Remember to do `.startciyk`"
    )

@bot.command()
async def showciyk(ctx):
    ciyk_text = get_ciyk_text(ctx, ciyk)

    await ctx.send(
        f"Below is what will be released at {format_datetime(ciyk.release_datetime)} in <#{ciyk.channel_id}>. " +
        "Remember to do `.startciyk`"
    )

    await ctx.send(ciyk_text)

@bot.command()
async def startpuzz(ctx):
    puzzles.releasing = True
    await ctx.send(
        f"Starting... Puzzle release set for {format_datetime(puzzles.release_datetime)}. " +
        "Do `.stoppuzz` if you want to stop the release."
    )

    now = datetime.datetime.now()
    wait_time = (puzzles.release_datetime - now).total_seconds()
    
    puzzles_channel = bot.get_channel(puzzles.channel_id)
    puzz_text = get_puzz_text(ctx, puzzles)
    
    await asyncio.sleep(wait_time+1)

    if not puzzles.releasing:
        return

    await puzzles_channel.send(puzz_text)
    for i in range(num_puzzles):
        await puzzles_channel.send(puzzles.urls[i])
    
    puzzles.change_week(puzzles.week_count + 1)

@bot.command()
async def stoppuzz(ctx):
    puzzles.releasing = False
    await ctx.send(f"The puzzles set for {format_datetime(puzzles.release_datetime)} will no longer be released.")

@bot.command()
async def startsb(ctx):
    sb.releasing = True
    await ctx.send(
        f"Starting... Second Best release set for {format_datetime(sb.release_datetime)}. " + 
        "Do `.stopsb` if you want to stop the release."
    )

    wait_time = (sb.release_datetime - datetime.datetime.now()).total_seconds()

    await asyncio.sleep(wait_time+1)

    if not sb.releasing:
        return

    sb_channel = bot.get_channel(sb.channel_id)
    sb_text = get_sb_text(ctx, sb)

    await sb_channel.send(sb_text)
    sb.change_week(sb.week_count + 1)

@bot.command()
async def stopsb(ctx):
    sb.releasing = False
    await ctx.send(f"The Second Best game set for {format_datetime(sb.release_datetime)} will no longer be released.")

@bot.command()
async def startciyk(ctx):
    ciyk.releasing = True
    await ctx.send(
        f"Starting... CIYK release set for {format_datetime(ciyk.release_datetime)}. " + 
        "Do `.stopciyk` if you want to stop the release."
    )

    wait_time = (ciyk.release_datetime - datetime.datetime.now()).total_seconds()

    ciyk_channel = bot.get_channel(ciyk.channel_id)
    ciyk_text = get_ciyk_text(ctx, ciyk)

    await asyncio.sleep(wait_time+1)

    if not ciyk.releasing:
        return

    await ciyk_channel.send(ciyk_text)
    ciyk.change_week(ciyk.week_count + 1)

@bot.command()
async def stopciyk(ctx):
    ciyk.releasing = False
    await ctx.send(f"The CIYK set for {format_datetime(ciyk.release_datetime)} will no longer be released.")

# changes the week count for the weekly puzzles in case it increments when it's not supposed to
# also used when a new semester begins
@bot.command()
async def changeweek(ctx, new_week_str):
    # check if the new week is a number
    try:
        new_week = int(new_week_str)

        puzzles.change_week(new_week)
        ciyk.change_week(new_week)
        sb.change_week(new_week)

    except ValueError:
        await ctx.send("A number must be used as the argument for this command.")

bot.run(TOKEN)