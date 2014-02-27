import re
from anorak import fanzub, regex, sabnzbd


class Downloader:
    
    def __init__(self):
        self.anime = None
        self.episode = None
        self.matched = []
        self.regexParser = regex.NameParser()
    def download(self):
        # reset matched
        self.matched = []
        # Strip symbols from anime name making it easier to get more relevant search results
        symbols = '[.!,;?]'
        # check for x-jat title override
        if self.anime.alternativeTitle != None and len(self.anime.alternativeTitle) > 0:
            friendlyName = re.sub(symbols, '', self.anime.alternativeTitle)
        else:
            friendlyName = re.sub(symbols, '', self.anime.title)

        search = fanzub.search(self.anime.subber, friendlyName, self.episode)

        for item in search:
            #print "%s, %s" % (item.name, item.url)
            regexParser = self.regexParser.parse(item.name)
            # match the series name case insensitively
            if regexParser.series_name.lower() != self.anime.title.lower() and regexParser.series_name.lower() != self.anime.alternativeTitle.lower():
                continue
            # match the episode number & convert to int first because we might have left hand zeroes
            if int(regexParser.ab_episode_numbers[0]) != int(self.episode):
                continue
            # no quality, user knows group only does one release quality
            if self.anime.quality == 0:
                self.matched.append(item)
                continue
            # match the quality
            if str(self.anime.quality) in regexParser.extra_info:
                self.matched.append(item)

        print "Found %s matches" % len(self.matched)

        try:
            url = self.matched[0].url
            name = self.matched[0].name
            return sabnzbd.SABnzbd(name, url)
        except IndexError:
            return False