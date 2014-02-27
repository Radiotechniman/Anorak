import threading
import time
import datetime
import random
from anorak import metadata, settings, model
from anorak.downloader import *


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
            print "Anorak searcher thread has woken up\n"
            animes = model.get_animes()
            refreshMetadata = self.date < datetime.datetime.now()
            for anime in animes:
                # refresh anime metadata only once a day at a random hour (so we don't DDOS anidb)
                if refreshMetadata:
                    metadata.refreshForAnime(anime.id)
                    time.sleep(60) # Sleep for 60 seconds so we don't trigger flood protection and get a temporary ban
                self.searchAnime(anime)
            if refreshMetadata:
                self.setMetadataRefreshDate()
            print "Anorak searcher thread resuming sleep\n"
            # reload settings just in case the search frequency changed
            self.settings = settings.getSettings()
            time.sleep(60*float(self.settings.get("Anorak", "searchFrequency")))
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