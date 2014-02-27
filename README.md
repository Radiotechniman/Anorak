Anorak
=====

*Anorak was designed for my personal usage. The features you want may not be present and it may contain bugs.*

Anorak is an automated downloader for newsgroup users. It watches for new episodes of your favorite anime shows and when they are posted it downloads them, sorts and renames them. It currently supports fanzub.com and retrieves show information from aniDB.net.

Notes:

There's no auto-updating mechanism. It is planned and will come later.


There is no management feature. This isn't planned at the moment.

Features include:

* automatically retrieves new episode nzb files
* sends NZBs directly to SABnzbd and categorizes them properly
* available for any platform, uses simple HTTP interface
* can notify Plex when new episodes are downloaded
* can move episodes to a folder specified using SABnzbd post-processing script included
* can specify a quality to download
* pick your favorite release group for subs
* allows easy override of search terms in case release name is different than the aniDB official name

Anorak makes use of the following projects:

* [pyanihttp][anidb]
* [webpy][webpy]

## Dependencies

To run Anorak from source you will need Python 2.7+. Hasn't been tested with Python 3.

## Bugs
Only tested on OS X and Safari.


When a release uses 10bit or 8bit in the name it causes quality checking to fail.


If you find a bug please report it or it'll never get fixed. Verify that it hasn't already been submitted and then log a new bug. Be sure to provide as much information as possible.

[anidb]: https://github.com/mineo/pyanihttp
[webpy]: http://webpy.org