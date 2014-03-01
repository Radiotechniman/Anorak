import threading
import time
import datetime
import random
from anorak import metadata, settings, model
from anorak.downloader import *

class MetadataRefreshThread(threading.Thread):
    def __init__(self, animes):
        threading.Thread.__init__(self)
        self.animes = animes
    def run(self):
        for anime in self.animes:
            try:
                metadata.refreshForAnime(anime.id)
            except:
                pass
            time.sleep(60) # Sleep for 60 seconds so we don't trigger flood protection and get a temporary ban
        return 0

class SearchThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.downloader = Downloader()
        self.settings = settings.getSettings()
        self.setMetadataRefreshDate()

    def setMetadataRefreshDate(self):
        tomorrow = datetime.datetime.now()+datetime.timedelta(days=1)
        year = tomorrow.year
        month = tomorrow.month
        day = tomorrow.day
        hour = random.choice(range(1,24))
        self.date = datetime.datetime(year, month, day, hour)

    def run(self):
        while (True):
            try:
                print "Anorak searcher thread has woken up\n"
                animes = list(model.get_animes())
                for anime in animes:
                    self.searchAnime(anime)
                # refresh anime metadata only once a day at a random hour (so we don't DDOS anidb)
                if self.date < datetime.datetime.now():
                    refresher = MetadataRefreshThread(animes)
                    refresher.start()
                    self.setMetadataRefreshDate()
                print "Anorak searcher thread resuming sleep\n"
                # reload settings just in case the search frequency changed
                self.settings = settings.getSettings()
                time.sleep(60*float(self.settings.get("Anorak", "searchFrequency")))
            except:
                print "Something went wrong with the searching thread. Continuing anyways."
    def searchAnime(self, anime):
        snatched = False
        print "Searching for newly aired anime in %s\n" % (anime.title)
        episodes = model.get_episodes(anime.id)
        for episode in episodes:
            if episode.wanted == 1:
                if episode.airdate != None:
                    if episode.airdate < datetime.datetime.now():
                        print "Attempting to snatch episode %s" % episode.episode
                        self.downloader.anime = anime
                        self.downloader.episode = episode.episode
                        if (self.downloader.download()):
                            model.snatched_episode(anime.id, episode.episode)
                            print "Episode was successfully snatched"
                            snatched = True
        return snatched