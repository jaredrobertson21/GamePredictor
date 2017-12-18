"""
Run this script to update the TeamStats model with the latest statistics for each team.
Specify the date(s) to be updated in the __main__ function.
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamepredictor.settings')

import django
django.setup()

import datetime
from django.db.models import F
from games.models import TeamStats
from grab_scores import get_game_information


# Provide a date range
def update_records(start_date, end_date=None):
    print("Starting update_records...")
    # Get objects from GamesList table
    if end_date:
        game_objects = get_game_information(datetime.datetime.strptime(start_date, '%Y-%m-%d'),
                                            datetime.datetime.strptime(end_date, '%Y-%m-%d'))
    else:
        game_objects = get_game_information(datetime.datetime.strptime(start_date, '%Y-%m-%d'))
    print("Collected records...")
    game_results = evaluate_game_results(game_objects)
    game_records = evaluate_records(game_results)

    print("Updating database...")

    for team in game_records:
        TeamStats.objects.filter(team=team).update(wins=F('wins') + game_records[team]['wins'],
                                                   losses=F('losses') + game_records[team]['losses'],
                                                   otl=F('otl') + game_records[team]['otl'])

    print("Records updated!")
    return game_records


# This result should be passed to a dictionary containing the records of the teams in that date range
# This record of each team in this range should be added to the record in the TeamStats table

def evaluate_game_results(games):
    print('Starting evaluate_game_results...')
    # Iterate through all objects returned
    # Each evaluation should return the winning team and the losing team (and if OTL)
    game_results = []
    for game in games:
        game_result = {
            'winner': game.winner(),
            'loser': game.loser(),
            'overtime': game.is_overtime(),
        }
        game_results.append(game_result)

    return game_results


def evaluate_records(game_results):
    print("Starting evaluate_records...")
    team_records = {}
    for game in game_results:
        winner = game['winner']
        loser = game['loser']
        if winner not in team_records:
            team_records[winner] = {'wins': 0,
                                    'losses': 0,
                                    'otl': 0}
        if loser not in team_records:
            team_records[loser] = {'wins': 0,
                                   'losses': 0,
                                   'otl': 0}
        # update the record of the winner
        team_records[winner]['wins'] += 1
        # update the record of the loser
        if game['overtime']:
            team_records[loser]['otl'] += 1
        else:
            team_records[loser]['losses'] += 1

    return team_records

if __name__ == '__main__':
    update_records('2017-10-04', '2017-12-16')
