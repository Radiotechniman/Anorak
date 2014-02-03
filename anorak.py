import lib.web as web
import lib.anidb as anidb
import lib.newznab_python_wrapper as newznab
import model

urls = (
	'/', 'Index',
    '/anime/(\d+)', 'Anime',
	'/settings', 'Settings',
    '/search', 'Search',
	'/new', 'New',
	'/remove/(\d+)', 'Remove',
)

### Templates
t_globals = {
	'datestr': web.datestr
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
    
    def GET(self, id):
        """ List anime episodes """
        episodes = model.get_episodes(id)
        return render.anime(episodes)
        
class New:
    
    def POST(self):
        # process anime here, populate episodes table with info from anidb
        return render.new(title)

class Search:
    form = web.form.Form(
        web.form.Textbox('query', web.form.notnull,
        size=30,
        description=""),
        web.form.Button('Search'),
    )
    
    def GET(self):
        """ Search for Anime and add it """
        form = self.form()
        return render.search(form, None)
        
    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form, None)
        results = anidb.search(form.d.query)
        render.new(results, results)

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()