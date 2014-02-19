import os
import shutil
import model
import regex

def processEpisode(dirName, nzbName=None):
    for root, dirs, files in os.walk(dirName):    
        for file in files:
            processFileAgainstDatabase(file)
    shutil.rmtree(dirName)
            
def processFileAgainstDatabase(file):
    regexParser = regex.NameParser(file)
    anime = regexParser.parse()
    if anime.series_name and anime.episode_numbers:
        shutil.move(file, model.get_anime(anime.series_name).location)