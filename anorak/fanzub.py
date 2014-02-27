# Author: Dennis Lutter <lad1337@gmail.com>
# URL: https://github.com/lad1337/XDM-main-plugin-repo/
#
# This file is part of a XDM plugin.
#
# XDM plugin.
# Copyright (C) 2013  Dennis Lutter
#
# This plugin is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This plugin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.

import lib.anidb.requests as requests
import re
import xml.etree.ElementTree as ET

class Download:
    def __init__(self):
        self.url = None
        self.name = None
        self.size = None
        self.external_id = None

def search(group, anime, episode):
    payload = {"cat": "anime",
    "max": 100}
    downloads = []
    #payload['q'] = "[%s] %s - %s" % (group, anime, episode)
    payload['q'] = "%s %s %s" % (group, anime, episode)
    r = requests.get("http://fanzub.com/rss", params=payload)
    print("Fanzub final search for term %s url %s" % (payload['q'], r.url))
    try:
        xml = ET.fromstring(r.text)
        items = xml.findall("channel/item")
    except Exception:
        print("Error trying to load FANZUB RSS feed")

    for item in items:
        title = item.find("title").text
        if "- {:>02}".format(episode) not in title:
            continue
        url = item.find("link").text
        ex_id = re.search("/(\d+)", url).group(1)
        curSize = int(item.find("enclosure").attrib["length"])
        #print("Found on Fanzub: %s" % (title))
        d = Download()
        d.url = url
        d.name = title
        d.size = curSize
        d.external_id = ex_id
        downloads.append(d)

    return downloads