CREATE TABLE animes (id integer primary key, title text, subber text, quality integer, location text);

CREATE TABLE episodes (id integer, title text, episode integer, snatched integer);

CREATE TABLE SABnzbd (url text primary key, username text, password text, key text, category text);

CREATE TABLE Settings ()