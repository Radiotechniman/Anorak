CREATE TABLE animes (
id integer primary key,
title text, subber text,
quality integer,
location text
);

CREATE TABLE episodes (
id integer,
title text,
episode integer,
airdate timestamp,
wanted integer /*0 is skipped, 1 is wanted, 2 is snatched*/
);

CREATE TABLE SABnzbd (
url text primary key,
username text,
password text,
key text,
category text
);