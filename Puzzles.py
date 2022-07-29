class Puzzles:
    def __init__(self):
        self.puzzle_urls = [None, None, None]

        self.speed_bonus = -1

        self.submission_link = None

    def change_puzzles(self, urls):
        self.puzzle_urls = urls

    def change_bonus(self, new_bonus):
        self.speed_bonus = new_bonus

    def change_link(self, new_link):
        self.submission_link = new_link