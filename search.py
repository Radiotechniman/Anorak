from downloader import *
import datetime
import threading
import model
import time
import metadata
import ConfigParser

class SearchThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.downloader = Downloader()
        self.getSettings()

    # this function is for allowing the search thread to reload it's settings after it wakes in case the frequency changed
    def getSettings(self):
        self.settings = ConfigParser.ConfigParser()
        try:
            file = open("anorak.cfg", "r")
            self.settings.readfp(file)
            file.close()
        except IOError, e:
            print "Could not read configuration file: ", str(e)

    def run(self):
        while (True):
            print "Anorak searcher thread has woken up\n"
            animes = model.get_animes()
            for anime in animes:
                self.searchAnime(anime)
            print "Anorak searcher thread resuming sleep\n"
            # reload settings
            self.getSettings()
            time.sleep(60*float(self.settings.get("Anorak", "searchFrequency")))
    def searchAnime(self, anime):
        print "Searching for newly aired anime in %s\n" % (anime.title)
        episodes = model.get_episodes(anime.id)
        for episode in episodes:
            if episode.wanted == 1:
                if episode.airdate != None:
                    if episode.airdate < datetime.datetime.now():
                        print "Attempting to snatch episode %s" % episode.episode
                        self.downloader.anime = anime.title
                        self.downloader.group = anime.subber
                        self.downloader.episode = episode.episode
                        if (self.downloader.download()):
                            model.snatched_episode(id, episode.episode)
                            return "Snatched successfully"
                        else:
                            return "Couldn't snatch"
        #refresh metadata in the anime, look for new episode titles