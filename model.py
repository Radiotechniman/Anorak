import lib.web as web
import datetime

db = web.database(dbn='sqlite', db='anorak')

def get_animes():
    return db.select('animes', order='title DESC')
    
def get_anime(id):
    try:
        return db.select('animes', where='id=$id', vars=locals())[0]
    except IndexError:
        return None

def new_anime(id, title, group, quality=0):
    db.insert('animes', id=id, title=title, quality=quality)
    
def remove_anime(id):
    db.delete('animes', where='id=$id', vars=locals())
    # this may or may not delete all the episodes for the given anime
    db.delete('episodes', where='id=$id', vars=locals())
    
def snatched_episode(id, episode):
    db.update('episodes', where='id=$id AND episode=$episode', vars=locals(),
        snatched=1)
        
def update_episode(id, episode, title):
    db.update('episodes', where='id=$id AND episode=$episode', vars=locals(),
        title=title)

def new_episode(id, title, episode):
    db.insert('episodes', id=id, title=title, episode=episode, snatched=0)
    
def get_episodes(id):
    try:
        return db.select('episodes', where='id=$id', vars=locals())
    except IndexError:
        return None

def remove_episode(id, episode):
    db.delete(episodes, where='id=$id AND episode=$episode', vars=locals())