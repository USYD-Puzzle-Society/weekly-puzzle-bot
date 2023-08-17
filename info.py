import os
import json
import discord
import datetime
from discord.ext import commands

class Info():
    def __init__(self):
        self.info_fn = "info.json" # fn = filename
        self.datetime_format = "%d/%m/%Y %H:%M"

        if os.path.exists(self.info_fn):
            with open(self.info_fn, "r") as fn:
                self.info = json.load(fn)
        else:
            self.info = {
                "emojis": {
                    "jigsaw": ":jigsaw:",
                    "brain": ":brain:",
                    "speech": ":speech_balloon:",
                    "heart": ":heart:",
                    "cross": ":x:"
                },
                "rebuscryptic": {
                    "role_name": "weekly puzzles",
                    "channel_id": 892032997220573204,
                    "release_datetime": "08/08/2022 12:00",
                    "week_num": -1,
                    "img_urls": [],
                    "submission_link": "",
                    "releasing": False
                },
                "minipuzz": {
                    "role_name": "weekly puzzles",
                    "channel_id": 892032997220573204,
                    "release_datetime": "08/08/2022 12:00",
                    "week_num": -1,
                    "img_urls": [],
                    "submission_link": "",
                    "interactive_link": "",
                    "releasing": False
                },
                "crossword": {
                    "role_name": "crosswords",
                    "channel_id": 1074683905405358171,
                    "release_datetime": "08/08/2022 12:00",
                    "week_num": -1,
                    "img_urls": [],
                    "submission_link": "",
                    "releasing": False
                },
                "wordsearch": {
                    "role_name": "word searches",
                    "channel_id": 1135184991928721448,
                    "release_datetime": "08/08/2022 12:00",
                    "week_num": -1,
                    "img_urls": [],
                    "submission_link": "",
                    "releasing": False
                },
                "logicpuzz": {
                    "role_name": "logic puzzles",
                    "channel_id": 1074684130794672138,
                    "release_datetime": "08/08/2022 12:00",
                    "week_num": -1,
                    "img_urls": [],
                    "submission_link": "",
                    "releasing": False
                },
                "ciyk": {
                    "role_name": "weekly games",
                    "channel_id": 1001742058601590824,
                    "discuss_id": 1001742642427744326,
                    "release_datetime": "08/08/2022 12:00",
                    "week_num": -1,
                    "img_url": "",
                    "submission_link": "",
                    "releasing": False
                }
            }
        
        self.minipuzz_datetime = self.str_to_datetime(self.info["minipuzz"]["release_datetime"])
        self.ciyk_datetime = self.str_to_datetime(self.info["ciyk"]["release_datetime"])

        self.day_names = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }

    # expects the %d/%m/%Y %H:%M format
    def str_to_datetime(self, string: str) -> datetime.datetime:
        date, time = string.split()

        day, month, year = date.split("/")
        hour, minute = time.split(":")

        return datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))

    def check_is_date(self, msg: str):
        try:
            strday, strmonth, stryear = msg.split("/")

            # check if it is a valid date
            date = datetime.date(int(stryear), int(strmonth), int(strday))

            day, month, year = int(strday), int(strmonth), int(stryear)

            return day, month, year
        
        except ValueError:
            return False

    def check_is_time(self, msg: str):
        try:
            strhour, strminute = msg.split(":")

            # check if valid time
            time = datetime.time(int(strhour), int(strminute))

            hour, minute = int(strhour), int(strminute)

            return hour, minute

        except ValueError:
            return False

    # each get_text function needs to read from the json file since the info could have been updated
    # this could potential pose problems if a read and write occur at the same time
    # however, this shouldn't be a big issue as the commands that use these functions will only be accessible by a few people

    def get_rebuscryptic_text(self, ctx: commands.context.Context, mention: bool) -> str:
        with open(self.info_fn, "r") as fn:
            self.info = json.load(fn)

        puzz_info = self.info["rebuscryptic"]
        role_name = puzz_info["role_name"]

        if mention:
            puzz_tag = f"{discord.utils.get(ctx.guild.roles, name=role_name).mention}\n\n"
        else:
            puzz_tag = f"@/{discord.utils.get(ctx.guild.roles, name=role_name)}\n\n"

        lines = [
            puzz_tag,
            f"**WEEKLY PUZZLE COMPETITION: WEEK {puzz_info['week_num']}**\n",
            "**REBUS + CRYPTIC**\n\n",
            "_Hints will be unlimited after the top 3 solvers have finished!_\n\n",
            f"Submit your answers here: {puzz_info['submission_link']}\n\n",
            "_You can submit as many times as you want!_\n",
            "_Your highest score will be kept._"
        ]

        return "".join(lines)

    # mention lets the function know whether the role should be tagged
    def get_minipuzz_text(self, ctx: commands.context.Context, mention: bool) -> str:
        with open(self.info_fn, "r") as fn:
            self.info = json.load(fn)
        
        puzz_info = self.info["minipuzz"]
        role_name = puzz_info["role_name"]

        if mention:
            puzz_tag = f"{discord.utils.get(ctx.guild.roles, name=role_name).mention}\n\n"
        else:
            puzz_tag = f"@/{discord.utils.get(ctx.guild.roles, name=role_name)}\n\n"

        lines = [
            puzz_tag,
            f"**WEEKLY PUZZLE COMPETITION: WEEK {puzz_info['week_num']}**\n",
            "**MINI-PUZZLE**\n\n",
            "_Hints will be unlimited after the top 3 solvers have finished!_\n\n",
            f"Submit your answers here: {puzz_info['submission_link']}\n\n",
            "_You can submit as many times as you want!_\n",
            "_Your highest score will be kept._"
        ]

        interactive_link = puzz_info["interactive_link"]
        if interactive_link:
            lines.append(f"\n\nInteractive version: {interactive_link}")

        return "".join(lines)
    
    def get_crossword_text(self, ctx: commands.context.Context, mention: bool) -> str:
        with open(self.info_fn, "r") as fn:
            self.info = json.load(fn)
        
        crossword_info = self.info["crossword"]
        role_name = crossword_info["role_name"]

        if mention:
            crossword_tag = f"{discord.utils.get(ctx.guild.roles, name=role_name).mention}\n\n"
        else:
            crossword_tag = f"@/{discord.utils.get(ctx.guild.roles, name=role_name)}\n\n"

        lines = [
            crossword_tag,
            f"**MIDI CROSSWORD: WEEK {crossword_info['week_num']}**"
        ]

        return "".join(lines)
    
    def get_wordsearch_text(self, ctx: commands.context.Context, mention: bool) -> str:
        with open(self.info_fn, "r") as fn:
            self.info = json.load(fn)

        wordsearch_info = self.info["wordsearch"]
        role_name = wordsearch_info["role_name"]

        if mention:
            wordsearch_tag = f"{discord.utils.get(ctx.guild.roles, name=role_name).mention}\n\n"
        else:
            wordsearch_tag = f"@/{discord.utils.get(ctx.guild.roles, name=role_name)}\n\n"

        lines = [
            wordsearch_tag,
            f"**WORD SEARCH: WEEK {wordsearch_info['week_num']}**"
        ]

        return "".join(lines)
    
    def get_logicpuzz_text(self, ctx: commands.context.Context, mention: bool) -> str:
        with open(self.info_fn, "r") as fn:
            self.info = json.load(fn)

        logicpuzz_info = self.info["logicpuzz"]
        role_name = logicpuzz_info["role_name"]

        if mention:
            logicpuzz_tag = f"{discord.utils.get(ctx.guild.roles, name=role_name).mention}\n\n"
        else:
            logicpuzz_tag = f"@/{discord.utils.get(ctx.guild.roles, name=role_name)}\n\n"

        lines = [
            logicpuzz_tag,
            f"**LOGIC PUZZLE: WEEK {logicpuzz_info['week_num']}**"
        ]

        return "".join(lines)

    def get_ciyk_text(self, ctx: commands.context.Context, mention: bool) -> str:
        with open(self.info_fn, "r") as fn:
            self.info = json.load(fn)

        emojis = self.info["emojis"]
        ciyk_info = self.info["ciyk"]
        role_name = ciyk_info["role_name"]

        if mention:
            ciyk_tag = f"{discord.utils.get(ctx.guild.roles, name=role_name).mention}\n\n"
        else:
            ciyk_tag = f"@/{discord.utils.get(ctx.guild.roles, name=role_name)}\n\n"

        line1 = f'**COMMENT IF YOU KNOW: WEEK {ciyk_info["week_num"]}**\n\n'
        line2 = f'If you think you know the pattern, comment an answer that follows it in <#{ciyk_info["discuss_id"]}>\n'
        line3 = f'We\'ll react with a {emojis["heart"]} if you\'re right and a {emojis["cross"]} if you\'re wrong!\n\n'

        return ciyk_tag + line1 + line2 + line3 + ciyk_info["img_url"]

    def get_text(self, ctx: commands.context.Context, puzz_name: str, mention: bool):
        get_text = {
            "rebuscryptic": self.get_rebuscryptic_text,
            "minipuzz": self.get_minipuzz_text,
            "crossword": self.get_crossword_text,
            "wordsearch": self.get_wordsearch_text,
            "logicpuzz": self.get_logicpuzz_text,
            "ciyk": self.get_ciyk_text,
        }

        return get_text[puzz_name](ctx, mention)

    # this method exists as just an easy way to change the data in one method call in setpuzzles/setciyk    
    def change_data(self, puzz_name: str, new_data: "dict[str, any]"):
        self.info[puzz_name]["week_num"] = new_data["week_num"]
        self.info[puzz_name]["submission_link"] = new_data["submission_link"]

        if "ciyk" == puzz_name:
            self.info[puzz_name]["img_url"] = new_data["img_url"]
        elif "minipuzz" == puzz_name:
            self.info[puzz_name]["img_urls"] = new_data["img_urls"]
            self.info[puzz_name]["interactive_link"] = new_data["interactive_link"]
        else:
            self.info[puzz_name]["img_urls"] = new_data["img_urls"]

        # write the new info to the json file so that it is not lost if the bot shuts down
        with open(self.info_fn, "w") as info:
            new_json = json.dumps(self.info, indent=4)

            info.write(new_json)
    
    def change_time(self, puzz_name: str, new_time: datetime.datetime):
        self.info[puzz_name]["release_datetime"] = new_time.strftime(self.datetime_format)
        
        with open(self.info_fn, "w") as info:
            new_json = json.dumps(self.info, indent=4)

            info.write(new_json)

    # changes the state of whether a puzzle is releasing
    def change_release(self, puzz_name: str, is_releasing: bool):
        self.info[puzz_name]["releasing"] = is_releasing

        with open(self.info_fn, "w") as info:
            new_json = json.dumps(self.info, indent=4)

            info.write(new_json)