import lib.web as web
import lib.anidb as anidb
import sys
import model
import datetime
import search
import metadata
import process
import ConfigParser
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
    '/refresh/(\d+)', 'Refresh',
    '/process', 'Process',
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

settings = ConfigParser.ConfigParser()

try:
    file = open("anorak.cfg", "r")
    settings.readfp(file)
    file.close()
except IOError, e:
    print "Creating configuration file"

# Setup the default settings and create the sections
if not settings.has_section("Anorak"):
    settings.add_section("Anorak")
    settings.add_section("SABnzbd")
    settings.set("Anorak", "port", 26463)
    settings.set("Anorak", "searchFrequency", 30)
    settings.set("SABnzbd", "url", "http://localhost:8080/")
    settings.set("SABnzbd", "key", "")
    settings.set("SABnzbd", "category", "")
    settings.set("SABnzbd", "username", "")
    settings.set("SABnzbd", "password", "")
    file = open("anorak.cfg","w")
    settings.write(file)
    file.close()
    # Weirdness, settings must be reloaded from file or else ConfigParser throws a hissy fit
    file = open("anorak.cfg", "r")
    settings.readfp(file)
    file.close()

class Index:
    
    def GET(self):
        """ List anime """
        animes = model.get_animes()
        return render.index(animes)

class Anime:
    
    form = web.form.Form(
        web.form.Textbox('location', web.form.notnull,
        size=30,
        description="Location"),
        web.form.Button('Change'),
    )
    
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
        raise web.seeother('/anime/%s' % int(id))
        
class Remove:
    
    def GET(self, id):
        model.remove_anime(id)
        raise web.seeother('/')

class Refresh:

    def GET(self, id):
        metadata.refreshForAnime(int(id))
        raise web.seeother('/anime/%s' % id)
        
class Process:
    
    def GET(self):
        query = web.input()
        try:
            nzbName = query.nzbName
        except:
            nzbName = None
        if (process.processEpisode(query.dir, nzbName)):
            return "Successfully processed episode."
        return "Episode failed to process."

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
        
class Settings:
    
    sabnzbdForm = web.form.Form(
        web.form.Textbox('url', web.form.notnull,
        size=30,
        value=settings.get("SABnzbd", "url"),
        description="SABnzbd URL:"),

        web.form.Textbox('username',
        size=30,
        value=settings.get("SABnzbd", "username"),
        description="SABnzbd Username:"),

        web.form.Password('password',
        size=30,
        value=settings.get("SABnzbd", "password"),
        description="SABnzbd Password:"),

        web.form.Textbox('key', web.form.notnull,
        size=30,
        value=settings.get("SABnzbd", "key"),
        description="SABnzbd API key:"),

        web.form.Textbox('category',
        size=30,
        value=settings.get("SABnzbd", "category"),
        description="SABnzbd Category:"),

        web.form.Button('Update'),
    )

    settingsForm = web.form.Form(
        web.form.Textbox('port', web.form.notnull,
        size=30,
        value=str(settings.get("Anorak", "port")),
        description="Port Number:"),

        web.form.Textbox('searchFrequency', web.form.notnull,
        size=30,
        value=str(settings.get("Anorak", "searchFrequency")),
        description="Search Frequency:"),

        web.form.Button('Update'),
    )
    
    def GET(self):
        return render.settings(self.settingsForm, self.sabnzbdForm)
    
    def POST(self):
        if not self.sabnzbdForm.validates():
            return render.settings(self.settingsForm, self.sabnzbdForm)
        settings.set("Anorak", "searchFrequency", self.settingsForm.d.searchFrequency)
        settings.set("Anorak", "port", self.settingsForm.d.port)
        settings.set("SABnzbd", "url", self.sabnzbdForm.d.url)
        settings.set("SABnzbd", "username", self.sabnzbdForm.d.username)
        settings.set("SABnzbd", "password", self.sabnzbdForm.d.password)
        settings.set("SABnzbd", "key", self.sabnzbdForm.d.key)
        settings.set("SABnzbd", "category", self.sabnzbdForm.d.category)
        file = open("anorak.cfg","w")
        settings.write(file)
        file.close()
        return render.settings(self.settingsForm, self.sabnzbdForm)

app = web.application(urls, globals())
search = search.SearchThread()

if __name__ == '__main__':
    sys.argv[1:] = [settings.get("Anorak", "port")]
    search.start()
    app.run()