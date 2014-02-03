CREATE TABLE animes (
	id INT,
	title TEXT,
	group TEXT,
	quality INT,
	primary key (id)
);

CREATE TABLE episodes (
	id INT,
	title TEXT,
	episode INT,
	snatched INT,
	primary key (episode)
)

CREATE TABLE SABnzbd (
	url TEXT,
	port INT,
	key TEXT,
	category TEXT,
	primary key (url)
);