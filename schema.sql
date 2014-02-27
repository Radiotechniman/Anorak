CREATE TABLE animes (
    id integer primary key,
    title text,
    alternativeTitle text,
    subber text,
    quality integer, /* 0, 480, 720, 1080 */
    location text
);

CREATE TABLE episodes (
    id integer,
    title text,
    episode integer,
    airdate timestamp,
    wanted integer /*0 is skipped, 1 is wanted, 2 is snatched, 3 is downloaded*/
);