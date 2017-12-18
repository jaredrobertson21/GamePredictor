"""
Run this script to update the UserStats model with the latest scores.
Specify the date(s) to be updated in the __main__ function.
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamepredictor.settings')

import django
django.setup()

from games.models import GamesList, GamePredictions, UserStats
from django.db.models import F


def update_user_stats(start_date, end_date=None):
    """
    Updates the wins, losses, and overtime losses in the UserStats model
    for all users who made a prediction for the specified date.
    :param start_date: A date in the string format 'YYYY-MM-DD'
    :param end_date: Optional; A date in the string format 'YYYY-MM-DD'
    :return: None
    """

    # get game results, all predictions by user, and participating users from specified date
    if end_date:
        game_results = GamesList.objects.filter(game_date__range=[start_date, end_date])
        game_predictions = GamePredictions.objects.filter(game_date__range=[start_date, end_date])
        participating_users = GamePredictions.objects.filter(game_date__range=[start_date, end_date]).distinct('user_id')
    else:
        game_results = GamesList.objects.filter(game_date=start_date)
        game_predictions = GamePredictions.objects.filter(game_date=start_date)
        participating_users = GamePredictions.objects.filter(game_date=start_date).distinct('user_id')

    # initialize the game results dictionary; each game_id is a key
    game_results_dictionary = {}
    for game in game_results:
        game_results_dictionary[game.game_id] = {'winner': '',
                                                 'overtime': ''}

    # determine the winners and if the game went to overtime for each game_id, store in the dictionary
    for game in game_results:
        game_results_dictionary[game.game_id]['winner'] = game.winner()
        game_results_dictionary[game.game_id]['overtime'] = game.is_overtime()

    # initialize the each participating user's record for the day; each user is a key
    user_record_dictionary = {}
    for user in participating_users:
        user_record_dictionary[user.user_id_id] = {'wins': 0,
                                                'losses': 0,
                                                'otl': 0}

    # assign win's and losses for each prediction to the corresponding user
    for prediction in game_predictions:
        if prediction.prediction == game_results_dictionary[prediction.game_id]['winner']:
            user_record_dictionary[prediction.user_id_id]['wins'] += 1
        else:
            if game_results_dictionary[prediction.game_id]['overtime']:
                user_record_dictionary[prediction.user_id_id]['otl'] += 1
            else:
                user_record_dictionary[prediction.user_id_id]['losses'] += 1

    # update the UserStats database with the new stats based on the day's predictions
    for user in user_record_dictionary:
        UserStats.objects.filter(id_id=user).update(wins=F('wins') + user_record_dictionary[user]['wins'],
                                                       losses=F('losses') + user_record_dictionary[user]['losses'],
                                                       otl=F('otl') + user_record_dictionary[user]['otl'])

    return None

# Specify the date(s) to update the user stats
if __name__ == '__main__':
    update_user_stats('2017-12-14', '2017-12-16')
