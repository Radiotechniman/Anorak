import os
import shutil
from anorak import notify, regex, model, settings

def processEpisode(dirName, nzbName=None):
    print dirName
    success = False
    for root, dirs, files in os.walk(dirName):
        for file in files:
            if(processFileAgainstDatabase(dirName, file)):
                success = True
    if (success):
        shutil.rmtree(dirName)
        if (settings.getSettings().get("Plex", "enabled")):
            notify.update_plex()
    return success

            
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
                if not os.path.exists(anime_from_database.location):
                    os.makedirs(anime_from_database.location)
                shutil.move(os.path.join(dirName,file), os.path.join(anime_from_database.location, file))
                return True
            else:
                print "Anime not in database, bailing"
                return False