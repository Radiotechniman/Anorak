import lib.anidb as anidb
import model

def newAnime(anime):
    #anime = anidb.query(anidb.QUERY_ANIME, id)
    model.new_anime(anime.id, anime.titles['x-jat'][0].title, form.d.subber, quality=0)
    for i in xrange(anime.episodecount):
        if anime.episodes.has_key(str(i+1)):
            # Prevent None type from being compared with a date
            if anime.episodes[str(i+1)].airdate != None:
                if (anime.episodes[str(i+1)].airdate > datetime.datetime.now()):
                    # Mark as wanted as it hasn't aired yet
                    model.new_episode(anime.id, i+1, anime.episodes[str(i+1)].titles['en'][0].title, 1, anime.episodes[str(i+1)].airdate)
                else:
                    # Mark as skipped because it's already aired and we're adding. Assume we've seen this episode.
                    model.new_episode(anime.id, i+1, anime.episodes[str(i+1)].titles['en'][0].title, 0, anime.episodes[str(i+1)].airdate)
            else:
                # It doesn't have an airdate but that's probably because it doesn't have one yet. Mark as wanted.
                model.new_episode(anime.id, i+1, anime.episodes[str(i+1)].titles['en'][0].title, 1, anime.episodes[str(i+1)].airdate)
        else:
            # This episode is so far in the future it doesn't even have any information! It must be unaired. Mark as wanted. We'll definitely want to refresh the metadata at a later date for this one!
            model.new_episode(anime.id, i+1, "Episode "+str(i+1), 1)

def refreshForAnime(id):
    anime = anidb.query(anidb.QUERY_ANIME, id)
    episodes = list(model.get_episodes(id))

    # update episodes that have new information

    for episode in episodes:
        if episode.title[:7]=="Episode":
            if anime.episodes[str(episode.episode)] != None:
                model.update_episode(id, episode.episode, anime.episodes[str(episode.episode)].titles['en'][0].title, anime.episodes[str(episode.episode)].airdate)

    # there are new episodes, create them
    if len(episodes)<anime.episodecount:
        currentEpisodeCount = len(list(episodes))
        numberOfNewEpisodes = anime.episodecount-currentEpisodeCount
        for i in xrange(numberOfNewEpisodes):
            episodeNumber = currentEpisodeCount+(i+1)
            model.new_episode(anime.id, episodeNumber, anime.episodes[str(episodeNumber)].titles['en'][0].title, 1, anime.episodes[str(episodeNumber)].airdate)