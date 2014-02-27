import urllib
import httplib
import ConfigParser


def SABnzbd(title=None, nzburl=None):
    settings = ConfigParser.ConfigParser()
    try:
        file = open("anorak.cfg", "r")
        settings.readfp(file)
        file.close()
    except IOError, e:
        print "Could not read configuration file: ", str(e)

    HOST = settings.get("SABnzbd", "url")
    if not str(HOST)[:4] == "http":
        HOST = 'http://' + HOST
    if not str(HOST)[-1:] == "/":
        HOST = HOST + '/'

    params = {}

    params['mode'] = 'addurl'
    params['name'] = nzburl
    params['nzbname'] = title

    if len(settings.get("SABnzbd", "username")):
        params['ma_username'] = settings.get("SABnzbd", "username")
    if len(settings.get("SABnzbd", "password")):
        params['ma_password'] = settings.get("SABnzbd", "password")
    if len(settings.get("SABnzbd", "key")):
        params['apikey'] = settings.get("SABnzbd", "key")
    if len(settings.get("SABnzbd", "category")):
        params['cat'] = settings.get("SABnzbd", "category")

    #if settings.retention:
    #    params["maxage"] = settings.retention

## FUTURE-CODE
#    if settings.priority:
#        params["priority"] = settings.priority
    #if settings.preprocessor:
    params["script"] = "sabToAnorak.py"

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
