-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- creating tournament database, if it exists, drop it and create a new table
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- Create player table on tournament with id as Primary Key
CREATE TABLE IF NOT EXISTS player (
    id serial PRIMARY KEY,
    name text
);

-- creating match table with match_id as primary key and winner/loser as foreign key
CREATE TABLE IF NOT EXISTS match (
    match_id serial PRIMARY KEY,
    winner serial REFERENCES player(id) ON DELETE CASCADE ,
    loser serial REFERENCES player(id) ON DELETE CASCADE ,
    CHECK (winner <> loser)
);

-- view to get players list and their winning records
CREATE VIEW winner_view AS
    SELECT player.id, name , count(match.winner) as wins, count(total.id) as matches
    from player LEFT JOIN match on player.id = match.winner
    LEFT JOIN (select id, count(*) from player, match WHERE player.id = match.winner or player.id = match.loser group by id) as total
    ON total.id = player.id GROUP BY player.id ORDER BY wins desc;