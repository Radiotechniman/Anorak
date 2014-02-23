import sys
import autoProcessAnime

if len(sys.argv) < 2:
    print "No folder supplied - is this being called from Anorak?"
    sys.exit()
elif len(sys.argv) >= 3:
    autoProcessAnime.processEpisode(sys.argv[1], sys.argv[2])
else:
    autoProcessAnime.processEpisode(sys.argv[1])