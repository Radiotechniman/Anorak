import urllib
from xml.dom import minidom
from anorak import settings


def update_plex():
    _settings = settings.getSettings()
    host = _settings.get("Plex", "url")

    if host == None:
        print("No Plex Server host specified, check your settings")
        return False

    if not str(host)[:4] == "http":
        host = 'http://' + host
    if not str(host)[-1:] == "/":
        host = host + '/'

    print("Updating library for the Plex Media Server host: " + host)


    url = "%slibrary/sections" % host
    try:
        xml_sections = minidom.parse(urllib.urlopen(url))
    except IOError, e:
        print("Error while trying to contact Plex Media Server: " + ex(e))
        return False

    sections = xml_sections.getElementsByTagName('Directory')
    if not sections:
        print("Plex Media Server not running on: " + host)
        return False

    for s in sections:
        if s.getAttribute('type') == "show":
            url = "%slibrary/sections/%s/refresh" % (host, s.getAttribute('key'))
            try:
                urllib.urlopen(url)
            except Exception, e:
                print("Error updating library section for Plex Media Server: " + ex(e))
                return False

    return True