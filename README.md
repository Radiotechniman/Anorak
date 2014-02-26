Anorak
=====

*Anorak is currently an alpha release. There may be severe bugs in it and at any given time it may not work at all.*

Anorak is a PVR for newsgroup users. It watches for new episodes of your favorite anime shows and when they are posted it downloads them, sorts and renames them. It currently supports fanzub.com and retrieves show information from aniDB.net.

Disclaimer:

I've only coded what I've needed personally. I haven't written the quality check code so it pulls whatever it finds first using the search terms and will prefer whatever it sees first rather than picking 720p over 480p. It's next on my list to code. As such I've only been testing and had success with release groups that put out a single quality. There's also no auto-updating mechanism. That will come later.

Features include:

* automatically retrieves new episode nzb files
* sends NZBs directly to SABnzbd and categorizes them properly
* available for any platform, uses simple HTTP interface
* can notify Plex when new episodes are downloaded
* pick your favorite release group for subs
* allows easy override of search terms in case release name is different than the aniDB official name

Anorak makes use of the following projects:

* [pyanihttp][anidb]
* [webpy][webpy]

## Dependencies

To run Anorak from source you will need Python 2.7+. Hasn't been tested with Python 3.

## Bugs

If you find a bug please report it or it'll never get fixed. Verify that it hasn't [already been submitted] and then [log a new bug]. Be sure to provide as much information as possible.

[anidb]: https://github.com/mineo/pyanihttp
[webpy]: http://webpy.org