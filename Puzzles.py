class Puzzles:
    def __init__(self, num_puzzles, release_datetime):
        self.urls = [None for i in range(num_puzzles)]
        self.release_datetime = release_datetime
        self.role_id = 994945577718648956
        self.channel_id = 994948949536407612

        self.speed_bonus = -1

        self.submission_link = None

    def change_puzzles(self, urls: list[str]):
        self.urls = urls

    def change_channel_id(self, new_id: int):
        self.channel_id = new_id

    def change_bonus(self, new_bonus: int):
        self.speed_bonus = new_bonus

    def change_link(self, new_link: str):
        self.submission_link = new_link