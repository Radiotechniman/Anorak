import sys
import process

if len(sys.argv) < 2:
    print "No folder supplied - is this being called from Anorak?"
    sys.exit()
elif len(sys.argv) >= 3:
    process.processEpisode(sys.argv[1], sys.argv[2])
else:
    process.processEpisode(sys.argv[1])