import os, urllib, urllib2
import datetime
import httplib

import lib.web as web
import model

def SABnzbd(title=None, nzburl=None):
    settings = model.get_settings()

    HOST = settings.url
    if not str(HOST)[:4] == "http":
        HOST = 'http://' + HOST

    params = {}

    params['mode'] = 'addurl'
    params['name'] = nzburl
    params['nzbname'] = title

    if settings.username:
        params['ma_username'] = settings.username
    if settings.password:
        params['ma_password'] = settings.password
    if settings.key:
        params['apikey'] = settings.key
    if settings.category:
        params['cat'] = settings.category

    #if settings.retention:
    #    params["maxage"] = settings.retention

## FUTURE-CODE
#    if settings.priority:
#        params["priority"] = settings.prriority
    #if settings.preprocessor:
    params["script"] = "sabToAnorak.py"

    # Note: If the url doesn't contain a slash at the end this won't work
    URL = HOST + "api?" + urllib.urlencode(params) 

    # to debug because of api
    print('Request url for <a href="%s">SABnzbd</a>' % URL)

    try:
        request = urllib.urlopen(URL)
        print('Sending Nzbfile to SAB <a href="%s">URL</a>' % URL)
        print('Sending Nzbfile to SAB')
    except (EOFError, IOError), e:
        print("Unable to connect to SAB with URL: %s" % URL)
        return False

    except httplib.InvalidURL, e:
        print("Invalid SAB host, check your config. Current host: %s" % HOST)
        return False

    result = request.read().strip()
    if not result:
        print("SABnzbd didn't return anything.")
        return False

    print("Result text from SAB: " + result)
    if result == "ok":
        print(title + " sent to SAB successfully.")
        return True
    elif result == "Missing authentication":
        print("Incorrect username/password.")
        return False
    else:
        print("Unknown error: " + result)
        return False
