import lib.web as web
import lib.anidb as anidb
import model
import datetime
import search
from downloader import *
#setup database with sqlite3 anorak < schema.sql

urls = (
	'/', 'Index',
    '/anime/(\d+)', 'Anime',
	'/settings', 'Settings',
    '/search', 'Search',
	'/new/(\d+)', 'New',
    '/add/(\d+)', 'Add',
	'/remove/(\d+)', 'Remove',
)

searchForm = web.form.Form(
        web.form.Textbox('query',
        size=15,
        height="100%",
        description="",
        id="search"),
        web.form.Button('Search', 
        id="search_button"),
    )

### Templates
t_globals = {
	'datestr': web.datestr,
    'str': str,
    'len': len,
    'datetime': datetime,
    'searchForm': searchForm
}

#web.config.debug = False

render = web.template.render('templates', base='base', globals=t_globals)

anidb.set_client('anorakk', 1)

class Index:
    
    def GET(self):
        """ List anime """
        animes = model.get_animes()
        return render.index(animes)

class Anime:
    
    def episodeForm(self,episode=None):
        return web.form.Form(
            web.form.Hidden('episode', value=episode),
            web.form.Button('Try'),
        )
    
    def GET(self, id):
        """ List anime episodes """
        anime = model.get_anime(id)
        episodes = model.get_episodes(id)
        episodeForm = self.episodeForm
        return render.anime(anime, episodes, episodeForm)
        
    def POST(self, id):
        anime = model.get_anime(id)
        downloader = Downloader()
        downloader.anime = anime.title
        downloader.group = anime.subber
        downloader.episode = web.input().episode
        if (downloader.download()):
            model.snatched_episode(id, web.input().episode)
            return "Snatched successfully"
        else:
            return "Couldn't snatch"
        
class Add:
    
    form = web.form.Form(
        web.form.Textbox('subber', web.form.notnull,
        size=30,
        description="Enter the release group"),
        web.form.Button('Complete Add'),
    )
    
    anime = None
    
    def GET(self, id):
        """ Show the groups doing releases / Actually shows a lame number of episode list without titles """
        form = self.form()
        anime = anidb.query(anidb.QUERY_ANIME, int(id))
        return render.add(form, anime)
    
    def POST(self, id):
        form = self.form()
        anime = anidb.query(anidb.QUERY_ANIME, int(id))
        if not form.validates():
            return render.add(form, anime)
        model.new_anime(anime.id, anime.titles['x-jat'][0].title, form.d.subber, quality=0)
        for i in xrange(anime.episodecount):
            if anime.episodes.has_key(str(i+1)):
                # Prevent None type from being compared with a date
                if anime.episodes[str(i+1)].airdate != None:
                    if (anime.episodes[str(i+1)].airdate > datetime.datetime.now()):
                        # Mark as wanted as it hasn't aired yet
                        model.new_episode(anime.id, i, anime.episodes[str(i+1)].titles['en'][0].title, 1, anime.episodes[str(i+1)].airdate)
                    else:
                        # Mark as skipped because it's already aired and we're adding. Assume we've seen this episode.
                        model.new_episode(anime.id, i, anime.episodes[str(i+1)].titles['en'][0].title, 0, anime.episodes[str(i+1)].airdate)
                else:
                    # It doesn't have an airdate but that's probably because it doesn't have one yet. Mark as wanted.
                    model.new_episode(anime.id, i, anime.episodes[str(i+1)].titles['en'][0].title, 1, anime.episodes[str(i+1)].airdate)
            else:
                # This episode is so far in the future it doesn't even have any information! It must be unaired. Mark as wanted. We'll definitely want to refresh the metadata at a later date for this one!
                model.new_episode(anime.id, i, "Episode "+str(i+1), 1)
        raise web.seeother('/')
        
class New:
    
    def POST(self, id):
        # process anime here, populate episodes table with info from anidb
        model.new_anime(id, title, group, quality=0)
        return render.new(title)

class Search:
    
    """form = web.form.Form(
        web.form.Textbox('query', web.form.notnull,
        size=30,
        description=""),
        web.form.Button('Search'),
    )"""
    
    def GET(self):
        """ Search for Anime and add it """
        #form = self.form()
        return render.search(searchForm, None)
        
    def POST(self):
        #form = self.form()
        if not searchForm.validates():
            return render.search(searchForm, None)
        results = anidb.search(searchForm.d.query)
        searchForm.d.query = ""
        return render.search(searchForm, results)
        
class FakeSettings:
    
    def __init__(self):
        self.url=None
        self.port=None
        self.key=None
        self.category=None
        
class Settings:
    
    settings = model.get_settings()
    if (settings==None):
        # If we can't get the settings it will return a None type object.
        # FakeSettings replaces None an object with blank properties.
        settings = FakeSettings()
    
    form = web.form.Form(
        web.form.Textbox('url', web.form.notnull,
        size=30,
        value=settings.url,
        description="SABnzbd URL:"),
        web.form.Textbox('key', web.form.notnull,
        size=30,
        value=settings.key,
        description="API key:"),
        web.form.Textbox('category', web.form.notnull,
        size=30,
        value=settings.category,
        description="Category:"),
        web.form.Button('Update'),
    )
    
    def GET(self):
        #reload settings after page settings load
        settings = model.get_settings()
        if (settings==None):
            settings = FakeSettings()
    
        form = web.form.Form(
            web.form.Textbox('url', web.form.notnull,
            size=30,
            value=settings.url,
            description="SABnzbd URL:"),
            web.form.Textbox('key', web.form.notnull,
            size=30,
            value=settings.key,
            description="API key:"),
            web.form.Textbox('category', web.form.notnull,
            size=30,
            value=settings.category,
            description="Category:"),
            web.form.Button('Update'),
        )
        return render.settings(form)
    
    def POST(self):
        form = self.form()
        if not form.validates():
            return render.settings(form)
        model.update_settings(form.d.url, form.d.key, form.d.category)
        return render.settings(form)

app = web.application(urls, globals())
search = search.SearchThread()

if __name__ == '__main__':
    search.start()
    app.run()