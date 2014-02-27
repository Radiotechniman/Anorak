import lib.web as web
import datetime

db = web.database(dbn='sqlite', db='anorak.db')

def get_animes():
    return db.select('animes', order='title DESC')
    
def get_anime(id):
    try:
        return db.select('animes', where='id=$id', vars=locals())[0]
    except IndexError:
        return None
        
def get_anime_by_title(title):
    # Custom query to make sure the where is case-insensitive
    try:
        return db.query("SELECT * FROM animes WHERE LOWER(title)=LOWER(\'%s\')" % title)[0]
    except IndexError:
        # Don't give up, try the alternative title
        try:
            return db.query("SELECT * FROM animes WHERE LOWER(alternativeTitle)=LOWER(\'%s\')" % title)[0]
        except IndexError:
            return None

def new_anime(id, title, subber, location, quality=0):
    db.insert('animes', id=id, title=title, subber=subber, location=location, quality=quality)
    
def remove_anime(id):
    db.delete('animes', where='id=$id', vars=locals())
    db.delete('episodes', where='id=$id', vars=locals())

def update_anime(id, alternativeTitle, releaseGroup, location, quality):
    db.update('animes', where='id=$id', vars=locals(),
              alternativeTitle=alternativeTitle, subber=releaseGroup, location=location, quality=quality)
    
def snatched_episode(id, episode):
    db.update('episodes', where='id=$id AND episode=$episode', vars=locals(),
        wanted=2)

def downloaded_episode(id, episode):
    db.update('episodes', where='id=$id AND episode=$episode', vars=locals(),
        wanted=3)
        
def update_episode(id, episode, title, airdate):
    db.update('episodes', where='id=$id AND episode=$episode', vars=locals(),
        title=title, airdate=airdate)

def new_episode(id, episode, title=None, wanted=None, airdate=None):
    db.insert('episodes', id=id, airdate=airdate, title=title, episode=episode, wanted=wanted)
    
def get_episodes(id):
    try:
        return db.select('episodes', where='id=$id', vars=locals())
    except IndexError:
        return None

def remove_episode(id, episode):
    db.delete(episode, where='id=$id AND episode=$episode', vars=locals())