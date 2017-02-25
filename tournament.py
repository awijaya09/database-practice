#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def finishExecuting(DB, cur):
    cur.close()
    DB.close()

def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cur = DB.cursor()

    cur.execute("DELETE from match;")
    DB.commit()
    finishExecuting(DB, cur)

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cur = DB.cursor()

    cur.execute("DELETE FROM player")
    DB.commit()
    finishExecuting(DB, cur)


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cur = DB.cursor()

    cur.execute("SELECT count(*) as total from player")
    total = cur.fetchone()
    return int(total[0])

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    cur = DB.cursor()

    cur.execute("INSERT INTO player(name) values (%s)", (name,))
    DB.commit()
    finishExecuting(DB, cur)

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    cur = DB.cursor()

    cur.execute("SELECT player.id, name , count(match.result) as wins, count(total.id) as matches "
                "from player LEFT JOIN match on player.id = match.result "
                "LEFT JOIN (select id, count(*) from player, match WHERE player.id = match.player1 or player.id = match.player2 group by id) as total "
                "ON total.id = player.id GROUP BY player.id ORDER BY wins desc;")
    player_standing = cur.fetchall()
    finishExecuting(DB, cur)
    return player_standing

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    cur = DB.cursor()

    cur.execute("INSERT INTO match values(%s, %s, %s)", (winner,loser,winner,))
    DB.commit()
    finishExecuting(DB, cur)


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # 1. Get the list of players
    player_standing = playerStandings()
    list = []
    # 2. Iterate through the list to get the closest pair
    for i in range(0,len(player_standing),2):
            player1_id = player_standing[i][0]
            player1_name = player_standing[i][1]

            player2_id = ""
            player2_name = ""
            if i+1 < len(player_standing):
                player2_id = player_standing[i+1][0]
                player2_name = player_standing[i+1][1]

            tuple = (player1_id, player1_name, player2_id, player2_name)
    # 3. Append the pair to the list
            list.append(tuple)
    # 4. Return the list as a result
    return list
