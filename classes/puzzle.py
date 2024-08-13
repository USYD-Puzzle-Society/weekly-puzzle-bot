from dataclasses import dataclass
import discord


@dataclass
class BasePuzzle:
    release_channel: int
    release_time: str
    week: int
    image_urls: list
    display_name: str


@dataclass
class DiscussionPuzzle(BasePuzzle):
    type = "discussion"
    role_name: str
    discussion_channel: int

    def get_tag(self, guild: discord.Guild, mention: bool):
        if mention:
            tag = f"{discord.utils.get(guild.roles, name=self.role_name).mention}\n\n"
        else:
            tag = f"{discord.utils.get(guild.roles, name=self.role_name)}\n\n"

        return tag

    def get_text(self, guild: discord.Guild, mention: bool):
        lines = [
            self.get_tag(guild, mention),
            f"𝗖𝗢𝗠𝗠𝗘𝗡𝗧 𝗜𝗙 𝗬𝗢𝗨 𝗞𝗡𝗢𝗪: 𝗪𝗘𝗘𝗞{self.week}\n\n",
            f"If you think you know the pattern, comment an answer that follows it in <#{self.discussion_channel}>\n",
            f"We'll react with a :heart: if you're right and a :x: if you're wrong!\n\n"
        ]
        return " ".join(lines)


@dataclass
class ChillPuzzle(BasePuzzle):
    type = "chill"
    role_name: str
    interactive_link: str = ""

    def get_tag(self, guild: discord.Guild, mention: bool):
        if mention:
            tag = f"{discord.utils.get(guild.roles, name=self.role_name).mention}\n\n"
        else:
            tag = f"{discord.utils.get(guild.roles, name=self.role_name)}\n\n"

        return tag

    def get_text(self, guild: discord.Guild, mention: bool):
        lines = [
            self.get_tag(guild, mention),
            f"{self.display_name}: 𝗪𝗘𝗘𝗞 {self.week}"
        ]

        if self.interactive_link:
            lines.append(f"\n\nInteractive version: {self.interactive_link}")

        return " ".join(lines)


@dataclass
class WeeklyPuzzle(BasePuzzle):
    type = "weekly"
    role_name: str
    submission_link: str
    interactive_link: str = ""

    def get_tag(self, guild: discord.Guild, mention: bool):
        if mention:
            tag = f"{discord.utils.get(guild.roles, name=self.role_name).mention}\n\n"
        else:
            tag = f"{discord.utils.get(guild.roles, name=self.role_name)}\n\n"

        return tag

    def get_text(self, guild: discord.Guild, mention: bool):
        lines = [
            self.get_tag(guild, mention),
            f"𝗪𝗘𝗘𝗞𝗟𝗬 𝗣𝗨𝗭𝗭𝗟𝗘 𝗖𝗢𝗠𝗣𝗘𝗧𝗜𝗧𝗜𝗢𝗡: 𝗪𝗘𝗘𝗞 {self.week}\n",
            f"\\- {self.display_name} -\n\n",
            "_Hints will be unlimited after the top 3 solvers have finished!_\n\n",
            f"Submit your answers here: {self.submission_link}\n\n",
            "_You can submit as many times as you want!_\n",
            "_Your highest score will be kept._"
        ]

        if self.interactive_link:
            lines.append(f"\n\nInteractive version: {self.interactive_link}")

        return " ".join(lines)


@dataclass
class JFFPuzzle(BasePuzzle):
    type = "jff"
    submission_link: str
    interactive_link: str = ""

    def get_text(self, guild: discord.Guild, mention: bool):
        lines = [
            f"𝗝𝗨𝗦𝗧-𝗙𝗢𝗥-𝗙𝗨𝗡: 𝗪𝗘𝗘𝗞 {self.week}\n",
            f"\\- {self.display_name} -\n\n"
        ]
        return " ".join(lines)