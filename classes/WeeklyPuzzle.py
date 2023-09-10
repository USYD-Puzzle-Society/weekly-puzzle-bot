from datetime import datetime
from beanie import Document
from typing import Optional, List
from enum import Enum

class WeeklyPuzzleType(Enum):
    REBUS_CRYPTIC = 1
    MINIPUZZ = 2
    WORD_SEARCH = 3
    LOGIC_PUZZLE = 4
    CROSSWORD = 5

class WeeklyPuzzle(Document):
    """Base class for a weekly puzzle.

    Attributes:
        role_name: A string representing the role that should be pinged on puzzle release.
        channel_id: A number representing the id of the channel the puzzle is released into.
        release_datetime: A Datetime object representing the time the puzzle should be released.
        week_num: A number representing the semester week that the puzzle belongs to.
        img_urls: A List of URLs for any images that is attached with the puzzle.
        submission_link: A string representing the URL to a Google Form to submit the answer.
        releasing: Whether the puzzle is being released.
    """
    type: WeeklyPuzzleType
    role_name: Optional[str]
    channel_id: int
    release_datetime: datetime
    week_num: int
    img_urls: List[str]
    submission_link: str
    releasing: bool