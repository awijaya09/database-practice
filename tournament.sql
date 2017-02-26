-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- creating player table
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE IF NOT EXISTS player (
    id serial PRIMARY KEY,
    name text
);

-- creating match table
CREATE TABLE IF NOT EXISTS match (
    match_id serial PRIMARY KEY,
    player1 serial REFERENCES player(id),
    player2 serial REFERENCES player(id),
    result serial
);

-- view to get players list and their winning records
CREATE VIEW winner_view AS
    SELECT player.id, name , count(match.result) as wins, count(total.id) as matches
    from player LEFT JOIN match on player.id = match.result
    LEFT JOIN (select id, count(*) from player, match WHERE player.id = match.player1 or player.id = match.player2 group by id) as total
    ON total.id = player.id GROUP BY player.id ORDER BY wins desc;