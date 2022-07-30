class SecondBest:
    def __init__(self, release_time):
        self.img_url = None
        self.release_datetime = release_time
        self.role_id = 994945577718648956
        self.channel_id = 994948949536407612

    def change_url(self, new_url):
        self.img_url = new_url
    
    def change_release(self, new_release):
        self.release_datetime = new_release
    
    def change_role(self, new_role):
        self.role_id = new_role

    def change_channel(self, new_channel):
        self.channel_id = new_channel