import ConfigParser

# TODO: Refactor all of the settings default configuration inside anorak.py into here and make this a singleton
def getSettings():
    settings = ConfigParser.ConfigParser()
    try:
        file = open("anorak.cfg", "r")
        settings.readfp(file)
        file.close()
        return settings
    except IOError, e:
        print "Could not read configuration file: ", str(e)