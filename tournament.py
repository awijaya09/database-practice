#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print "Unable to connect to database"

def finishExecuting(DB, cur):
    cur.close()
    DB.close()

def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()


    cursor.execute("TRUNCATE TABLE match;")
    db.commit()
    finishExecuting(db, cursor)

def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()

    cursor.execute("TRUNCATE TABLE player CASCADE;")
    db.commit()
    finishExecuting(db, cursor)


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()

    cursor.execute("SELECT count(*) as total from player")
    total = cursor.fetchone()
    return int(total[0])

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    query = "INSERT INTO player(name) values (%s);"
    param = (name,)
    cursor.execute(query, param)
    db.commit()
    finishExecuting(db, cursor)

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
    db, cursor = connect()

    cursor.execute("select * from winner_view;")
    player_standing = cursor.fetchall()
    finishExecuting(db, cursor)
    return player_standing

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    query = "INSERT INTO match (winner, loser) values(%s, %s);"
    param = (winner,loser,)
    cursor.execute(query, param)
    db.commit()
    finishExecuting(db, cursor)


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
