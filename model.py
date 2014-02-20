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
    try:
        return db.query("SELECT * FROM animes WHERE LOWER(title)=LOWER(\'%s\')" % title)[0]
    except IndexError:
        return None

def new_anime(id, title, subber, quality=0):
    db.insert('animes', id=id, title=title, subber=subber, quality=quality)
    
def remove_anime(id):
    db.delete('animes', where='id=$id', vars=locals())
    # this may or may not delete all the episodes for the given anime
    db.delete('episodes', where='id=$id', vars=locals())
    
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
    db.delete(episodes, where='id=$id AND episode=$episode', vars=locals())
    
def update_settings(url, key, category=None, username=None, password=None):
    try:
        settings = db.select('SABnzbd', vars=locals())[0]
        # Updating doesn't work
        db.update('SABnzbd', where='url=$url', vars=locals(), url=url, key=key, category=category, username=username, password=password)
    except IndexError:
        db.insert('SABnzbd', url=url, key=key, category=category, username=username, password=password)
        
def get_settings():
    try:
        return db.select('SABnzbd', vars=locals())[0]
    except IndexError:
        return None