import re
#use https://github.com/lad1337/Sick-Beard/blob/anime/sickbeard/name_parser/parser.py

anime_ep_regexes = [
                    

               ('anime_ultimate',
                """
                ^(?:\[(?P<release_group>.+?)\][ ._-]*)
                (?P<series_name>.+?)[ ._-]+
                (?P<ep_ab_num>\d{1,3})
                (-(?P<extra_ab_ep_num>\d{1,3}))?[ ._-]+?
                (?:v(?P<version>[0-9]))?
                (?:[\w\.]*)
                (?:(?:(?:[\[\(])(?P<extra_info>\d{3,4}[xp]?\d{0,4}[\.\w\s-]*)(?:[\]\)]))|(?:\d{3,4}[xp]))
                (?:[ ._]?\[(?P<crc>\w+)\])?
                .*?
                """
                ),
               ('anime_standard',
               # [Group Name] Show Name.13-14
               # [Group Name] Show Name - 13-14
               # Show Name 13-14
               # [Group Name] Show Name.13
               # [Group Name] Show Name - 13
               # Show Name 13
               '''
               ^(\[(?P<release_group>.+?)\][ ._-]*)?                        # Release Group and separator
               (?P<series_name>.+?)[ ._-]+                                 # Show_Name and separator
               (?P<ep_ab_num>\d{1,3})                                       # E01
               (-(?P<extra_ab_ep_num>\d{1,3}))?                             # E02
               (v(?P<version>[0-9]))?                                       # version
               [ ._-]+\[(?P<extra_info>\d{3,4}[xp]?\d{0,4}[\.\w\s-]*)\]       # Source_Quality_Etc-
               (\[(?P<crc>\w{8})\])?                                        # CRC
               .*?                                                          # Separator and EOL
               '''),
                    
               ('anime_standard_round',
               # TODO examples
               # [Stratos-Subs]_Infinite_Stratos_-_12_(1280x720_H.264_AAC)_[379759DB]
               # [ShinBunBu-Subs] Bleach - 02-03 (CX 1280x720 x264 AAC)
               '''
               ^(\[(?P<release_group>.+?)\][ ._-]*)?                                    # Release Group and separator
               (?P<series_name>.+?)[ ._-]+                                              # Show_Name and separator
               (?P<ep_ab_num>\d{1,3})                                                   # E01
               (-(?P<extra_ab_ep_num>\d{1,3}))?                                         # E02
               (v(?P<version>[0-9]))?                                                   # version
               [ ._-]+\((?P<extra_info>(CX[ ._-]?)?\d{3,4}[xp]?\d{0,4}[\.\w\s-]*)\)     # Source_Quality_Etc-
               (\[(?P<crc>\w{8})\])?                                                    # CRC
               .*?                                                                      # Separator and EOL
               '''),
               
               ('anime_slash',
               # [SGKK] Bleach 312v1 [720p/MKV]
               '''
               ^(\[(?P<release_group>.+?)\][ ._-]*)? # Release Group and separator
               (?P<series_name>.+?)[ ._-]+           # Show_Name and separator
               (?P<ep_ab_num>\d{1,3})                # E01
               (-(?P<extra_ab_ep_num>\d{1,3}))?      # E02
               (v(?P<version>[0-9]))?                # version
               [ ._-]+\[(?P<extra_info>\d{3,4}p)     # Source_Quality_Etc-
               (\[(?P<crc>\w{8})\])?                 # CRC
               .*?                                   # Separator and EOL
               '''),
               
               ('anime_standard_codec',
               # [Ayako]_Infinite_Stratos_-_IS_-_07_[H264][720p][EB7838FC]
               # [Ayako] Infinite Stratos - IS - 07v2 [H264][720p][44419534]
               # [Ayako-Shikkaku] Oniichan no Koto Nanka Zenzen Suki Janain Dakara ne - 10 [LQ][h264][720p] [8853B21C]
               '''
               ^(\[(?P<release_group>.+?)\][ ._-]*)?                        # Release Group and separator
               (?P<series_name>.+?)[ ._]*                                   # Show_Name and separator
               ([ ._-]+-[ ._-]+[A-Z]+[ ._-]+)?[ ._-]+                       # funny stuff, this is sooo nuts ! this will kick me in the butt one day
               (?P<ep_ab_num>\d{1,3})                                       # E01
               (-(?P<extra_ab_ep_num>\d{1,3}))?                             # E02
               (v(?P<version>[0-9]))?                                       # version
               ([ ._-](\[\w{1,2}\])?\[[a-z][.]?\w{2,4}\])?                        #codec
               [ ._-]*\[(?P<extra_info>(\d{3,4}[xp]?\d{0,4})?[\.\w\s-]*)\]    # Source_Quality_Etc-
               (\[(?P<crc>\w{8})\])?
               .*?                                                          # Separator and EOL
               '''),
               
               ('anime_and_normal',
               # Bleach - s16e03-04 - 313-314
               # Bleach.s16e03-04.313-314
               # Bleach s16e03e04 313-314
               '''
               ^(?P<series_name>.+?)[ ._-]+                 # start of string and series name and non optinal separator
               [sS](?P<season_num>\d+)[. _-]*               # S01 and optional separator
               [eE](?P<ep_num>\d+)                          # epipisode E02
               (([. _-]*e|-)                                # linking e/- char
               (?P<extra_ep_num>\d+))*                      # additional E03/etc
               ([ ._-]{2,}|[ ._]+)                          # if "-" is used to separate at least something else has to be there(->{2,}) "s16e03-04-313-314" would make sens any way
               (?P<ep_ab_num>\d{1,3})                       # absolute number
               (-(?P<extra_ab_ep_num>\d{1,3}))?             # "-" as separator and anditional absolute number, all optinal
               (v(?P<version>[0-9]))?                       # the version e.g. "v2"
               .*?
               '''

               ),
               ('anime_and_normal_x',
               # Bleach - s16e03-04 - 313-314
               # Bleach.s16e03-04.313-314
               # Bleach s16e03e04 313-314
               '''
               ^(?P<series_name>.+?)[ ._-]+                 # start of string and series name and non optinal separator
               (?P<season_num>\d+)[. _-]*               # S01 and optional separator
               [xX](?P<ep_num>\d+)                          # epipisode E02
               (([. _-]*e|-)                                # linking e/- char
               (?P<extra_ep_num>\d+))*                      # additional E03/etc
               ([ ._-]{2,}|[ ._]+)                          # if "-" is used to separate at least something else has to be there(->{2,}) "s16e03-04-313-314" would make sens any way
               (?P<ep_ab_num>\d{1,3})                       # absolute number
               (-(?P<extra_ab_ep_num>\d{1,3}))?             # "-" as separator and anditional absolute number, all optinal
               (v(?P<version>[0-9]))?                       # the version e.g. "v2"
               .*?
               '''

               ),
               
               ('anime_and_normal_reverse',
               # Bleach - 313-314 - s16e03-04
               '''
               ^(?P<series_name>.+?)[ ._-]+                 # start of string and series name and non optinal separator
               (?P<ep_ab_num>\d{1,3})                       # absolute number
               (-(?P<extra_ab_ep_num>\d{1,3}))?             # "-" as separator and anditional absolute number, all optinal
               (v(?P<version>[0-9]))?                       # the version e.g. "v2"
               ([ ._-]{2,}|[ ._]+)                          # if "-" is used to separate at least something else has to be there(->{2,}) "s16e03-04-313-314" would make sens any way
               [sS](?P<season_num>\d+)[. _-]*               # S01 and optional separator
               [eE](?P<ep_num>\d+)                          # epipisode E02
               (([. _-]*e|-)                                # linking e/- char
               (?P<extra_ep_num>\d+))*                      # additional E03/etc
               .*?
               '''
               ),
               
               ('anime_and_normal_front',
               # 165.Naruto Shippuuden.s08e014
               '''
               ^(?P<ep_ab_num>\d{1,3})                       # start of string and absolute number
               (-(?P<extra_ab_ep_num>\d{1,3}))?              # "-" as separator and anditional absolute number, all optinal
               (v(?P<version>[0-9]))?[ ._-]+                 # the version e.g. "v2"
               (?P<series_name>.+?)[ ._-]+
               [sS](?P<season_num>\d+)[. _-]*                 # S01 and optional separator
               [eE](?P<ep_num>\d+) 
               (([. _-]*e|-)                               # linking e/- char
               (?P<extra_ep_num>\d+))*                      # additional E03/etc
               .*?
               '''
               ),
                ('anime_ep_name',
                 """
                ^(?:\[(?P<release_group>.+?)\][ ._-]*)
                (?P<series_name>.+?)[ ._-]+
                (?P<ep_ab_num>\d{1,3})
                (-(?P<extra_ab_ep_num>\d{1,3}))?[ ._-]*?
                (?:v(?P<version>[0-9])[ ._-]+?)?
                (?:.+?[ ._-]+?)?
                \[(?P<extra_info>\w+)\][ ._-]?
                (?:\[(?P<crc>\w{8})\])?
                .*?
                 """
                ),
               ('anime_bare',
               # One Piece - 102
               # [ACX]_Wolf's_Spirit_001.mkv
               '''
               ^(\[(?P<release_group>.+?)\][ ._-]*)?
               (?P<series_name>.+?)[ ._-]+                         # Show_Name and separator
               (?P<ep_ab_num>\d{3})                                      # E01
               (-(?P<extra_ab_ep_num>\d{3}))?                            # E02
               (v(?P<version>[0-9]))?                                     # v2
               .*?                                                         # Separator and EOL
               ''')
               ]
class NameParser(object):
    def __init__(self, file_name=True, regexMode=0):
        
            self.file_name = file_name
            self.compiled_regexes = []
            self._compile_regexes(regexMode)
    def _parse_string(self, name):
        
            if not name:
                return None
        
            for (cur_regex_name, cur_regex) in self.compiled_regexes:
                match = cur_regex.match(name)

                if not match:
                    #logger.log(u"No match found for '"+cur_regex_name+"' in '"+name+"'",logger.DEBUG)
                    continue
            
            
                result = ParseResult(name)
                result.which_regex = [cur_regex_name]
            
                named_groups = match.groupdict().keys()
                #logger.log(u"Matched: named_groups: "+str(named_groups)+" using '"+str(cur_regex_name)+"' in '"+name+"'",logger.DEBUG)
            
                if 'series_name' in named_groups:
                    result.series_name = match.group('series_name')
                    if result.series_name:
                        result.series_name = self.clean_series_name(result.series_name)
            
                if 'season_num' in named_groups:
                    tmp_season = int(match.group('season_num'))
                    if cur_regex_name == 'bare' and tmp_season in (19,20):
                        continue
                    result.season_number = tmp_season
            
                if 'ep_num' in named_groups:
                    ep_num = self._convert_number(match.group('ep_num'))
                    if 'extra_ep_num' in named_groups and match.group('extra_ep_num'):
                        result.episode_numbers = range(ep_num, self._convert_number(match.group('extra_ep_num'))+1)
                    else:
                        result.episode_numbers = [ep_num]
                    
                if 'ep_ab_num' in named_groups:
                    ep_ab_num = self._convert_number(match.group('ep_ab_num'))
                    if 'extra_ab_ep_num' in named_groups and match.group('extra_ab_ep_num'):
                        result.ab_episode_numbers = range(ep_ab_num, self._convert_number(match.group('extra_ab_ep_num'))+1)
                    else:
                        result.ab_episode_numbers = [ep_ab_num]

                if 'air_year' in named_groups and 'air_month' in named_groups and 'air_day' in named_groups:
                    year = int(match.group('air_year'))
                    month = int(match.group('air_month'))
                    day = int(match.group('air_day'))
                
                    # make an attempt to detect YYYY-DD-MM formats
                    if month > 12:
                        tmp_month = month
                        month = day
                        day = tmp_month

                    try:
                        result.air_date = datetime.date(year, month, day)
                    except ValueError, e:
                        raise InvalidNameException(e.message)

                if 'extra_info' in named_groups:
                    tmp_extra_info = match.group('extra_info')
                
                    # Show.S04.Special is almost certainly not every episode in the season
                    if tmp_extra_info and cur_regex_name == 'season_only' and re.match(r'([. _-]|^)(special|extra)\w*([. _-]|$)', tmp_extra_info, re.I):
                        continue
                    result.extra_info = tmp_extra_info
            
                if 'release_group' in named_groups:
                    result.release_group = match.group('release_group')

                return result
    def _compile_regexes(self,regexMode):
            for (cur_pattern_name, cur_pattern) in anime_ep_regexes:
                try:
                    cur_regex = re.compile(cur_pattern, re.VERBOSE | re.IGNORECASE)
                except re.error, errormsg:
                    print(u"WARNING: Invalid episode_pattern, %s. %s" % (errormsg, cur_pattern))
                else:
                    self.compiled_regexes.append((cur_pattern_name, cur_regex))
    def parse(self,name):
        # break it into parts if there are any (dirname, file name, extension)
        dir_name, file_name = os.path.split(name)
        ext_match = re.match('(.*)\.\w{3,4}$', file_name)
        
        if ext_match and self.file_name:
            base_file_name = ext_match.group(1)
        else:
            base_file_name = file_name
        
        return self._parse_string(base_file_name)
                    
class ParseResult(object):
    def __init__(self,
                 original_name,
                 series_name=None,
                 season_number=None,
                 episode_numbers=None,
                 extra_info=None,
                 release_group=None,
                 air_date=None,
                 ab_episode_numbers=None
                 ):

        self.original_name = original_name
        
        self.series_name = series_name
        self.season_number = season_number
        if not episode_numbers:
            self.episode_numbers = []
        else:
            self.episode_numbers = episode_numbers

        if not ab_episode_numbers:
            self.ab_episode_numbers = []
        else:
            self.ab_episode_numbers = ab_episode_numbers

        self.extra_info = extra_info
        self.release_group = release_group
        
        self.air_date = air_date
        
        self.which_regex = None
        
    def __eq__(self, other):
        if not other:
            return False
        
        if self.series_name != other.series_name:
            return False
        if self.season_number != other.season_number:
            return False
        if self.episode_numbers != other.episode_numbers:
            return False
        if self.extra_info != other.extra_info:
            return False
        if self.release_group != other.release_group:
            return False
        if self.air_date != other.air_date:
            return False
        if self.ab_episode_numbers != other.ab_episode_numbers:
            return False
        
        return True

    def __str__(self):
        if self.series_name != None:
            to_return = self.series_name + u' - '
        else:
            to_return = u''
        if self.season_number != None:
            to_return += 'S'+str(self.season_number)
        if self.episode_numbers and len(self.episode_numbers):
            for e in self.episode_numbers:
                to_return += 'E'+str(e)

        if self.air_by_date:
            to_return += 'abd: '+str(self.air_date)
        if self.ab_episode_numbers:
            to_return += ' absolute_numbers: '+str(self.ab_episode_numbers)

        if self.extra_info:
            to_return += u' - ' + unicode(self.extra_info)
        if self.release_group:
            to_return += ' (' + self.release_group + ')'

        to_return += ' [ABD: '+str(self.air_by_date)+']'
        to_return += ' [ANIME: '+str(self.is_anime)+']' 
        to_return += ' [whichReg: '+str(self.which_regex)+']'

        return to_return.encode('utf-8')

    def _is_air_by_date(self):
        if self.season_number == None and len(self.episode_numbers) == 0 and self.air_date:
            return True
        return False
    air_by_date = property(_is_air_by_date)
    
    def _is_anime(self):
        if self.ab_episode_numbers:
            return True
        return False
    is_anime = property(_is_anime)

    def _sxxexx(self):
        return bool(self.season_number != None and self.episode_numbers)

    sxxexx = property(_sxxexx)