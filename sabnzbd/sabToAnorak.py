import sys
import autoProcess

if len(sys.argv) < 2:
    print "No folder supplied - is this being called from Anorak?"
    sys.exit()
elif len(sys.argv) >= 3:
    autoProcess.processEpisode(sys.argv[1], sys.argv[2])
else:
    autoProcess.processEpisode(sys.argv[1])