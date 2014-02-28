import sys
import datetime
import ConfigParser
import lib.web as web
import lib.anidb as anidb
from anorak.downloader import *
from anorak import metadata, model, process, search

urls = (
	'/', 'Index',
	'/anime/(\d+)', 'Anime',
	'/settings', 'Settings',
	'/search', 'Search',
	'/add/(\d+)', 'Add',
	'/remove/(\d+)', 'Remove',
	'/refresh/(\d+)', 'Refresh',
	'/process', 'Process',
	'/shutdown', 'Shutdown'
)

searchForm = web.form.Form(
        web.form.Textbox('query',
        web.form.notnull,
        size=15,
        height="100%",
        description="",
        id="search"),
        web.form.Button('Search', 
        id="search_button"),
    )

def setupDatabase():
    import os
    if not os.path.exists('anorak.db'):
        import sqlite3
        conn = sqlite3.connect('anorak.db')
        c = conn.cursor()
        schema = open('schema.sql', 'r').read()
        c.executescript(schema)
        conn.commit()
        c.close()

def getConfig():
    try:
        file = open("anorak.cfg", "r")
        settings.readfp(file)
        file.close()
    except IOError, e:
        print "Creating configuration file"
        setupConfig()

def setupConfig():
    # Setup the default settings and create the sections
    if not settings.has_section("Anorak"):
        settings.add_section("Anorak")
        settings.add_section("SABnzbd")
        settings.add_section("Plex")
        settings.set("Anorak", "port", 26463)
        settings.set("Anorak", "searchFrequency", 30)
        settings.set("SABnzbd", "url", "localhost:8080")
        settings.set("SABnzbd", "key", "")
        settings.set("SABnzbd", "category", "")
        settings.set("SABnzbd", "username", "")
        settings.set("SABnzbd", "password", "")
        settings.set("Plex", "url", "localhost:32400")
        settings.set("Plex", "enabled", False)
        file = open("anorak.cfg","w")
        settings.write(file)
        file.close()
        # Weirdness, settings must be reloaded from file or else ConfigParser throws a hissy fit
        file = open("anorak.cfg", "r")
        settings.readfp(file)
        file.close()

### Templates
t_globals = {
	'datestr': web.datestr,
    'str': str,
    'len': len,
    'datetime': datetime,
    'searchForm': searchForm,
    'createTitleListing': metadata.createTitleListing
}

#web.config.debug = False

render = web.template.render('templates', base='base', globals=t_globals)

anidb.set_client('anorakk', 1)

settings = ConfigParser.ConfigParser()

getConfig()
setupDatabase()

class Index:
    
    def GET(self):
        """ List anime """
        animes = model.get_animes()
        return render.index(animes)

class Anime:

    def episodeForm(self,episode=None):
        return web.form.Form(
            web.form.Hidden('episode', value=episode),
            web.form.Hidden('form', value="episode"),
            #web.form.Button('Try'),
        )

    def editorForm(self,anime):
        return web.form.Form(
            web.form.Textbox('location', web.form.notnull,
            size=30,
            value=anime.location,
            description="Location:"),

            web.form.Textbox('alternativeTitle',
            size=30,
            value=anime.alternativeTitle,
            description="Name override (for searching only):"),

            web.form.Textbox('releaseGroup',
            size=30,
            value=anime.subber,
            description="Release Group:"),

            web.form.Dropdown('quality',
            [('0', 'None'), ('720', '720p'), ('480', '480p'), ('1080', '1080p')],
            value=str(anime.quality),
            description="Force a quality. Leave 'None' if your release group doesn't have more than one quality."),

            web.form.Hidden('form', value="editor"),

            web.form.Button('Update'),
        )
    
    def GET(self, id):
        """ List anime episodes """
        anime = model.get_anime(id)
        episodes = model.get_episodes(id)
        editorForm = self.editorForm(anime)
        return render.anime(anime, episodes, self.episodeForm, editorForm)
        
    def POST(self, id):
        i = web.input()

        # assuming that the name of the hidden field is "form"
        if i.form == "editor":
            return self.POST_editor(id)
        else:
            return self.POST_snatch(id)

    def POST_snatch(self, id):
        anime = model.get_anime(id)
        downloader = Downloader()
        downloader.anime = anime
        downloader.episode = web.input().episode
        if (downloader.download()):
            model.snatched_episode(id, web.input().episode)
            return "Snatched successfully"
        else:
            return "Couldn't snatch episode %s" % web.input().episode

    def POST_editor(self, id):
        anime = model.get_anime(id)
        episodes = model.get_episodes(id)
        editorForm = self.editorForm(anime)
        if not editorForm.validates():
            return render.anime(anime,episodes,self.episodeForm,editorForm)
        model.update_anime(id, web.input().alternativeTitle, web.input().releaseGroup, web.input().location, int(web.input().quality))
        return render.anime(anime,episodes,self.episodeForm,editorForm)
        
class Add:
    
    form = web.form.Form(
        web.form.Dropdown('quality',
        [(0, 'None'), (720, '720p'), (480, '480p'), (1080, '1080p')],
        description="Force a quality. Leave 'None' if your release group doesn't have more than one quality."),

        web.form.Textbox('subber', web.form.notnull,
        size=30,
        description="Enter the release group"),

        web.form.Textbox('location', web.form.notnull,
        size=30,
        description="Enter the file path for storing episodes"),

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
        metadata.newAnime(anime, form.d.subber, form.d.location, form.d.quality)
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
    
    def GET(self):
        """ Search for Anime and add it """
        return render.search(None)
        
    def POST(self):
        if not searchForm.validates():
            return render.search(None)
        results = anidb.search(searchForm.d.query)
        return render.search(results)
        
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

        web.form.Hidden('form', value="sabnzbd"),

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

        web.form.Hidden('form', value="settings"),

        web.form.Button('Update'),
    )

    plexForm = web.form.Form(
        web.form.Checkbox('enabled',
        checked=settings.getboolean("Plex", "enabled"),
        description="Plex Enabled:"),

        web.form.Textbox('url', web.form.notnull,
        size=30,
        value=str(settings.get("Plex", "url")),
        description="Plex URL:"),

        web.form.Hidden('form', value="plex"),

        web.form.Button('Update'),
    )
    
    def GET(self):
        return render.settings(self.settingsForm, self.sabnzbdForm, self.plexForm)
    
    def POST(self):
        i = web.input()

        # determine which form to process based on the hidden value "form"
        if i.form == "settings":
            return self.POST_settings()
        if i.form == "sabnzbd":
            return self.POST_sabnzbd()
        if i.form == "plex":
            return self.POST_plex()

    def POST_settings(self):
        if not self.settingsForm.validates():
            return render.settings(self.settingsForm, self.sabnzbdForm, self.plexForm)
        settings.set("Anorak", "searchFrequency", self.settingsForm.d.searchFrequency)
        settings.set("Anorak", "port", self.settingsForm.d.port)
        file = open("anorak.cfg","w")
        settings.write(file)
        file.close()
        return render.settings(self.settingsForm, self.sabnzbdForm)

    def POST_sabnzbd(self):
        if not self.sabnzbdForm.validates():
            return render.settings(self.settingsForm, self.sabnzbdForm, self.plexForm)
        settings.set("SABnzbd", "url", self.sabnzbdForm.d.url)
        settings.set("SABnzbd", "username", self.sabnzbdForm.d.username)
        settings.set("SABnzbd", "password", self.sabnzbdForm.d.password)
        settings.set("SABnzbd", "key", self.sabnzbdForm.d.key)
        settings.set("SABnzbd", "category", self.sabnzbdForm.d.category)
        file = open("anorak.cfg","w")
        settings.write(file)
        file.close()
        return render.settings(self.settingsForm, self.sabnzbdForm, self.plexForm)

    def POST_plex(self):
        if not self.plexForm.validates():
            return render.settings(self.settingsForm, self.sabnzbdForm, self.plexForm)
        settings.set("Plex", "url", self.plexForm.d.url)
        settings.set("Plex", "enabled", self.plexForm.d.enabled)
        file = open("anorak.cfg","w")
        settings.write(file)
        file.close()
        return render.settings(self.settingsForm, self.sabnzbdForm, self.plexForm)

class Shutdown(object):
    def GET(self):
        sys.exit(0)

app = web.application(urls, globals())
search = search.SearchThread()

if __name__ == '__main__':
    port = settings.get("Anorak", "port")
    sys.argv[1:] = [port]
    search.start()
    app.run()