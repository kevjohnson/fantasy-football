"""
This script uses the nflgame library to download game stats for every player
and calculate the number of fantasy points they scored in each game.

The two inputs are the `seasons` and `weeks` variables in the `main` method.
These should be a list (or generator) of the years and weeks you want the data
for.  The script defaults to every regular season game from 2009 to 2014.
"""
import nflgame
import csv
from pprint import pprint

# Dictionary that stores default scoring values for most leagues.
score = {
    "passing_yds": 1. / 25.,
    "passing_tds": 4,
    "passint_int": -1,
    "passint_tpm": 2,
    "rushing_yds": 1. / 10.,
    "rushing_tds": 6,
    "rushing_tpm": 2,
    "receiving_yds": 1. / 10.,
    "receiving_tds": 6,
    "receiving_tpm": 2,
    "fumbles_lost": -2,
    "fumbles_rec_tds": 6,
    "kickret_tds": 6,
    "puntret_tds": 6
}


def main():
    """
    Call getFantasyPoints() for the given seasons and weeks.  Output results to
    a csv file.
    """
    seasons = xrange(2009, 2015)
    weeks = xrange(1, 18)
    data = getFantasyPoints(seasons, weeks)
    fname = str(seasons[0]) + "-" + str(seasons[-1]) + ".csv"
    variables = ["season", "week", "id", "name",
                 "pos", "team", "points", "opponent"]
    with open(fname, "wb") as outFile:
        writer = csv.writer(outFile)
        writer.writerow(variables)
        for season in data:
            for week in data[season]:
                for player in data[season][week]:
                    writer.writerow([season, week] + player)


def getFantasyPoints(seasons, weeks):
    """
    Download game stats for every season and week and calculate the fantasy
    points scored for each player in each game.

    Args:
        seasons (list): List of seasons (int).
        weeks (list): List of weeks (int).

    Returns:
        dict: Dictionary of fantasy points scored.
    """
    data = {}
    schedule = nflgame.sched.games
    for s in seasons:
        print s
        data[s] = {}
        for w in weeks:
            games = nflgame.games(s, w)
            players = nflgame.combine_game_stats(games)
            data[s][w] = []
            positions = ["QB", "RB", "WR", "TE"]
            gen = (p for p in players if p.player.position in positions)
            for player in gen:
                points = calculateFantasyPoints(player)
                points.append(getOpponent(schedule, s, w, player))
                data[s][w].append(points)
    return data


def calculateFantasyPoints(player):
    """
    Calculate the fantasy points scored by a given player.

    Args:
        player (GamePlayerStats): Object with stats for a player in a game.

    Returns:
        list: List with player id, name, position, team, and points scored.
    """
    # Get set of available stats of interest for this player
    stats = set(player.stats).intersection(set(score))

    # Multiply the player's stats by the corresponding scoring value
    points = round(sum(player.stats[k] * score[k] for k in stats), 2)

    return [player.playerid, player.name, player.player.position,
            player.player.team, points]


def getOpponent(schedule, season, week, player):
    """
    Retrieve a player's opponent in a given game

    Args:
        schedule (OrderedDict): Full NFL schedule.
        season (int): Year of game.
        week (int): Week of game.
        player (GamePlayerStats): Object with stats for a player in a game.

    Returns:
        str: The opponent of the give player in that game.
    """
    game = [schedule[k] for k in schedule
            if schedule[k]["year"] == season and
            schedule[k]["week"] == week and
            schedule[k]["season_type"] == "REG" and
            (schedule[k]["home"] == player.player.team or
             schedule[k]["away"] == player.player.team)]
    if not game:
        opponent = None
    elif game[0]["home"] == player.player.team:
        opponent = game[0]["away"]
    else:
        opponent = game[0]["home"]
    return opponent


if __name__ == '__main__':
    main()
