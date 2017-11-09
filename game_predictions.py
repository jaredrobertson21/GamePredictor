import database
from choice import Choice
from grab_scores import get_daily_games_list


def make_game_predictions(user, games):
    choices = Choice(user)
    for game in games:
        choice = input("Who will win: {} or {}?".format(game.home_team, game.away_team))
        choices.predictions[game.game_id] = choice
    return choices

conn = database.db_connect()
cursor = conn.cursor()
games = get_daily_games_list(cursor, '2017-11-07')
make_game_predictions(1, games)
conn.close()