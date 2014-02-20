import lib.web as web
import lib.anidb as anidb
import model
import datetime
import search
import metadata
from downloader import *
#setup database with sqlite3 anorak < schema.sql
"""
Setup database from some sort of wizard
import os
if not os.path.exists('anorak.db'):
    import sqlite3
    conn = sqlite3.connect('anorak.db')
    c = conn.cursor()
    schema = open('schema.sql', 'r').read()
    c.execute(schema)
    conn.commit()
    c.close()
"""

urls = (
	'/', 'Index',
    '/anime/(\d+)', 'Anime',
	'/settings', 'Settings',
    '/search', 'Search',
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
            return "Couldn't snatch episode %s" % web.input().episode
        
class Add:
    
    form = web.form.Form(
        web.form.Textbox('subber', web.form.notnull,
        size=30,
        description="Enter the release group"),
        web.form.Button('Complete Add'),
    )
    
    anime = None
    
    def GET(self, id):
        """ Show the groups doing releases (UDP only feature, we're using TCP) """
        form = self.form()
        anime = anidb.query(anidb.QUERY_ANIME, int(id))
        return render.add(form, anime)
    
    def POST(self, id):
        form = self.form()
        anime = anidb.query(anidb.QUERY_ANIME, int(id))
        if not form.validates():
            return render.add(form, anime)
        metadata.newAnime(anime)
        raise web.seeother('/')
        
class Remove:
    
    def GET(self, id):
        model.remove_anime(id)
        return "Anime %s removed from database" % id

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