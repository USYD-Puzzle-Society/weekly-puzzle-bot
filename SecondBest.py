class SecondBest:
    def __init__(self, release_time):
        self.img_url = "[Image]"
        self.release_datetime = release_time
        self.role_id = 994945577718648956
        self.channel_id = 994948949536407612

        self.submission_link = "[Link]"

        self.week_count = 1

        self.releasing = False

    def change_url(self, new_url: str):
        self.img_url = new_url
    
    def change_release(self, new_release):
        self.release_datetime = new_release
    
    def change_role(self, new_role: int):
        self.role_id = new_role

    def change_channel(self, new_channel: int):
        self.channel_id = new_channel

    def change_link(self, new_link: str):
        self.submission_link = new_link

    def change_week(self, new_week: int):
        self.week_count = new_week