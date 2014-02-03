CREATE TABLE animes (id integer primary key, title text, subber text, quality integer);

CREATE TABLE episode (id integer, title text, episode integer primary key, snatched integer);

CREATE TABLE SABnzbd (url text primary key, port integer, key text, category text);