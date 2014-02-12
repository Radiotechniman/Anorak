import fanzub
import sabnzbd

class Downloader:
    
    def __init__(self):
        self.anime = None
        self.episode = None
        self.group = None
    def download(self):
        search = fanzub.search(self.group, self.anime, self.episode)
        try:
            url = search[0].url
            name = search[0].name
            return sabnzbd.SABnzbd(name, url)
        except IndexError:
            return False