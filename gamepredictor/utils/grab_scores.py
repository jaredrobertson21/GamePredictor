import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamepredictor.settings')

import django
django.setup()

from games.models import GamesList
from game import ScheduleGame
import datetime
import requests
from bs4 import BeautifulSoup

schedule_url = "https://www.hockey-reference.com/leagues/NHL_2018_games.html"


def update_scores_in_db(start_date, end_date=None):
    """
    Adds the scores of completed games to the games_list database table. A range of dates can be specified.
    :param cursor: Database cursor
    :param start_date: Beginning date of score(s) to be updated (string, in the form 'YYYY-MM-DD')
    :param end_date: End date of scores to be updated (string, in the form 'YYYY-MM-DD'); default = None
    :return: None
    """
    if end_date:
        game_objects = get_game_information(datetime.datetime.strptime(start_date, '%Y-%m-%d'),
                                            datetime.datetime.strptime(end_date, '%Y-%m-%d'))
    else:
        game_objects = get_game_information(datetime.datetime.strptime(start_date, '%Y-%m-%d'))

    for game in game_objects:
        GamesList.objects.filter(game_id=game.game_id).update(away_team_score=game.away_team_score,
                                                              home_team_score=game.home_team_score,
                                                              overtime=game.overtime,
                                                              attendance=game.attendance)

    return None


def get_game_information(start_date, end_date=None):
    """
    Retrieves all game information, played or unplayed, for the specified interval. For only one day of games,
    just provide the start date.
    :param start_date: A datetime object, representing the earliest date of games to retrieve
    :param end_date: A datetime object, representing the latest date of games to retrieve
    :return: A list of ScheduleGame objects from the provided date range
    """
    html = get_html(schedule_url)
    games_list = html.find('tbody').find_all('tr')
    requested_game_information = []
    for game in games_list:
        game_date = datetime.datetime.strptime(game.find('th').get_text(), '%Y-%m-%d')
        if end_date:
            if start_date <= game_date <= end_date:
                requested_game_information.append(ScheduleGame(game))
        else:
            if game_date == start_date:
                requested_game_information.append(ScheduleGame(game))

    return requested_game_information


def get_html(url):
    req = requests.get(url)
    return BeautifulSoup(req.text, 'html.parser')

if __name__ == '__main__':
    update_scores_in_db('2017-12-10', '2017-12-13')

