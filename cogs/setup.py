import datetime
import discord
from discord.ext import commands
from discord import app_commands

import os
import json

from typing import Literal

EXEC_ROLE_NAME = "Executives"


class Setup(commands.GroupCog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.info_fp = "info.json"
        self.datetime_format = "%d/%m/%Y %H:%M"

        self.day_to_wpc_puzzles = {
            "Monday": "\- 𝗥𝗘𝗕𝗨𝗦 -",
            "Wednesday": "\- 𝗖𝗥𝗬𝗣𝗧𝗜𝗖 + 𝗟𝗢𝗚𝗜𝗖 -",
            "Friday": "\- 𝗠𝗜𝗡𝗜𝗣𝗨𝗭𝗭𝗟𝗘 -",
        }

        self.day_to_jff_puzzles = {
            "Monday": "\- 𝗥𝗘𝗕𝗨𝗦/𝗖𝗥𝗬𝗣𝗧𝗜𝗖 -",
            "Friday": "\- 𝗖𝗥𝗢𝗦𝗦𝗪𝗢𝗥𝗗/𝗙𝗥𝗘𝗘 -",
        }

        # technically inefficient way of doing this
        # but practically the semester only has 13 weeks
        # so this is faster to write
        self.bold_numbers = {
            1: "𝟭",
            2: "𝟮",
            3: "𝟯",
            4: "𝟰",
            5: "𝟱",
            6: "𝟲",
            7: "𝟳",
            8: "𝟴",
            9: "𝟵",
            10: "𝟭𝟬",
            11: "𝟭𝟭",
            12: "𝟭𝟮",
            13: "𝟭𝟯",
        }

        self.wpc_channel_id = 892032997220573204
        self.wpc_role_id = 892266410397548574

        self.jff_channel_id = 1266395033385435209

    def check_valid_time(self, release_time: str):
        release_hour, release_minute = release_time.split(":")
        release_hour, release_minute = int(release_hour), int(release_minute)

        if release_hour > 23 or release_hour < 0:
            return False
        if release_minute > 59 or release_minute < 0:
            return False

        return release_hour, release_minute

    # function to get the date that is the next occurrence of the
    # specified day. e.g if given dayname="Monday", function will return
    # the date of the next Monday
    def get_next_closest_day(
        self, dayname: str, release_hour: int, release_minute
    ) -> datetime.datetime:
        # the integer values of days as specified by datetime module
        day_ints = {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6,
        }

        now = datetime.datetime.now()
        # at most have to iterate through the next 8 days (including current day)
        for i in range(8):
            delta_date = now + datetime.timedelta(i)
            if delta_date.weekday() == day_ints[dayname]:
                return datetime.datetime(
                    delta_date.year,
                    delta_date.month,
                    delta_date.day,
                    release_hour,
                    release_minute,
                )

    def get_wpc_text(
        self,
        dayname: str,
        week_num: int,
        submission_link: str,
        interactive_link: str,
    ):
        lines = [
            f"\n\n𝗪𝗘𝗘𝗞𝗟𝗬 𝗣𝗨𝗭𝗭𝗟𝗘 𝗖𝗢𝗠𝗣𝗘𝗧𝗜𝗧𝗜𝗢𝗡: 𝗪𝗘𝗘𝗞 {self.bold_numbers[week_num]}\n",
            f"{self.day_to_wpc_puzzles[dayname]}\n\n",
            "_Hints will be unlimited after the top 3 solvers have finished!_\n\n",
            f"Submit your answers here: {submission_link}\n\n",
            "_You can submit as many times as you want!_\n",
            "_Your highest score will be kept._",
        ]

        if interactive_link:
            lines.append(f"\n\nInteractive Version: {interactive_link}")

        return "".join(lines)

    def get_jff_text(self, dayname: str, week_num: int, interactive_link: str):
        lines = [
            f"𝗝𝗨𝗦𝗧-𝗙𝗢𝗥-𝗙𝗨𝗡 𝗣𝗨𝗭𝗭𝗟𝗘𝗦: 𝗪𝗘𝗘𝗞 {self.bold_numbers[week_num]}\n",
            f"{self.day_to_jff_puzzles[dayname]}",
        ]

        if interactive_link:
            lines.append(f"\n\nInteractive Version: {interactive_link}")

        return "".join(lines)

    def write_release_info(
        self,
        dayname: str,
        release_text: str,
        release_datetime: str,
        img_urls: list[str],
        category: Literal["WPC", "JFF"],
    ):
        if os.path.exists(self.info_fp):
            with open(self.info_fp, "r") as f:
                info = json.load(f)

        puzz_data = {
            "release_text": release_text,
            "release_datetime": release_datetime,
            "img_urls": img_urls,
            "channel_id": "",
            "role_id": "",
            "releasing": False,
        }

        if category == "WPC":
            puzz_data["channel_id"] = self.wpc_channel_id
            puzz_data["role_id"] = self.wpc_role_id
        else:
            puzz_data["channel_id"] = self.jff_channel_id

        info[f"{dayname}{category}"] = puzz_data

        with open(self.info_fp, "w") as f:
            new_info = json.dumps(info, indent=4)
            f.write(new_info)

    async def get_image_urls(self, interaction: discord.Interaction):
        def message_from_user(msg):
            return msg.author == interaction.user

        await interaction.channel.send(
            "Please send all the images for the puzzle in one message."
            + " Type `exit` at any time to stop."
        )

        msg = await self.bot.wait_for("message", check=message_from_user)

        if "exit" == msg.content.lower():
            await interaction.followup.send(
                "Command stopped. No changes have been made."
            )
            return []

        while not len(msg.attachments):
            await interaction.followup.send(
                "Please send all the images for the puzzle in one message."
                + " Type `exit` at any time to stop."
            )

            msg = await self.bot.wait_for("message", check=message_from_user)

            if "exit" == msg.content.lower():
                await interaction.followup.send(
                    "Command stopped. No changes have been made."
                )
                return []

        return [image.url for image in msg.attachments]

    @app_commands.command(
        name="wpc",
        description="Set the info for the WPC release. Year of release is assumed to be the current year.",
    )
    @commands.has_role(EXEC_ROLE_NAME)
    async def set_wpc(
        self,
        interaction: discord.Interaction,
        release_day: Literal["Monday", "Wednesday", "Friday"],
        week_num: int,
        submission_link: str,
        interactive_link: str = "",
        release_time: str = "16:00",
    ):
        await interaction.response.defer()

        valid_time = self.check_valid_time(release_time)
        if not valid_time:
            await interaction.followup.send(
                "Please enter a valid time in the format HH:MM. Note that the release time is in 24 hour format."
            )
            return

        release_hour, release_minute = valid_time

        release_datetime = self.get_next_closest_day(
            release_day, release_hour, release_minute
        )

        release_text = self.get_wpc_text(
            release_day, week_num, submission_link, interactive_link
        )

        image_urls = await self.get_image_urls(interaction)

        await interaction.followup.send(
            f"Done! The following will be sent at {release_datetime.strftime(self.datetime_format)}\n\n"
            + f"@/{interaction.guild.get_role(self.wpc_role_id)}"
            + release_text
        )

        self.write_release_info(
            release_day,
            release_text,
            release_datetime.strftime(self.datetime_format),
            image_urls,
            "WPC",
        )

        await interaction.channel.send(f"Remember to do `/start wpc {release_day}`")

    @app_commands.command(
        name="jff",
        description="Set the info for the WPC release. Year of release is assumed to be the current year.",
    )
    @commands.has_role(EXEC_ROLE_NAME)
    async def set_jff(
        self,
        interaction: discord.Interaction,
        release_day: Literal["Monday", "Friday"],
        week_num: int,
        interactive_link: str = "",
        release_time: str = "16:00",
    ):
        await interaction.response.defer()

        valid_time = self.check_valid_time(release_time)
        if not valid_time:
            await interaction.followup.send(
                "Please enter a valid time in the format HH:MM. Note that the release time is in 24 hour format."
            )
            return

        release_hour, release_minute = valid_time

        release_datetime = self.get_next_closest_day(
            release_day, release_hour, release_minute
        )

        release_text = self.get_jff_text(release_day, week_num, interactive_link)

        image_urls = await self.get_image_urls(interaction)

        await interaction.followup.send(
            f"Done! The following will be sent at {release_datetime.strftime(self.datetime_format)}\n\n"
            + release_text
        )

        self.write_release_info(
            release_day,
            release_text,
            release_datetime.strftime(self.datetime_format),
            image_urls,
            "JFF",
        )

        await interaction.channel.send(f"Remember to do `/start jff {release_day}`")

    # @app_commands.command(name="edit", description="Edit puzzle information.")
    # @commands.has_role(EXEC_ROLE_NAME)
    # async def edit_puzzle(
    #     self,
    #     interaction: discord.Interaction,
    #     puzzle_type: Literal["WPC", "JFF"],
    #     current_release_day: Literal[
    #         "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    #     ],
    #     new_image: discord.Attachment = None,
    #     new_image2: discord.Attachment = None,
    #     new_release_day: Literal[
    #         "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    #     ] = None,
    #     new_release_time: str = None,
    #     new_submission_link: str = None,
    #     new_interactive_link: str = None,
    # ):
    #     await interaction.response.defer()

    #     if os.path.exists(self.info_fp):
    #         with open(self.info_fp, "r") as f:
    #             info = json.load(f)
    #     else:
    #         await interaction.followup.send(
    #             f"No puzzles have been setup. Use `/setup {puzzle_type}`."
    #         )
    #         return

    #     try:
    #         puzz_data = info[f"{current_release_day}{puzzle_type}"]
    #     except KeyError:
    #         await interaction.followup.send(
    #             f"The {current_release_day} {puzzle_type} has not been setup. Use `/setup {puzzle_type}`"
    #         )
    #         return

    #     new_img_urls = []
    #     if new_image:
    #         new_img_urls.append(new_image.url)
    #     if new_image2:
    #         new_img_urls.append(new_image2.url)
    #     if new_img_urls:
    #         puzz_data["img_urls"] = new_img_urls


async def setup(bot: commands.Bot):
    await bot.add_cog(Setup(bot))
