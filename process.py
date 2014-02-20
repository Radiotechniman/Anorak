import os
import shutil
import model
import regex
import urlparse

def processEpisode(dirName, nzbName=None):
    print dirName
    for root, dirs, files in os.walk(dirName):
        for file in files:
            processFileAgainstDatabase(dirName, file)
    shutil.rmtree(dirName)
            
def processFileAgainstDatabase(dirName, file):
    regexParser = regex.NameParser()
    anime = regexParser.parse(file)
    if not anime == None:
        if anime.series_name and anime.ab_episode_numbers:
            print "Found %s episode %s from %s" % (anime.series_name, anime.ab_episode_numbers[0], anime.release_group)
            anime_from_database = model.get_anime_by_title(anime.series_name)
            if not anime_from_database == None:
                print "Anime matched database, moving"
                model.downloaded_episode(anime_from_database.id, anime.ab_episode_numbers[0])
                shutil.move(os.path.join(dirName,file), anime_from_database.location)
            else:
                print "Anime not in database, bailing"