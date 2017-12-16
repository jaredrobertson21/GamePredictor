import datetime
import requests
from bs4 import BeautifulSoup
#from .game import ScheduleGame, Game
from .models import GamesList

root_url = 'https://hockey-reference.com'
schedule_url = "https://www.hockey-reference.com/leagues/NHL_2018_games.html"


def get_html(url):
    req = requests.get(url)
    return BeautifulSoup(req.text, 'html.parser')


def get_games_results():
    """
    Retrieves all games results from the previous day
    :return: a list of dictionaries with the keys: winner, winner_score, loser, loser_score
    """
    html = get_html(schedule_url)
    games_summary = html.find_all(class_='game_summary')
    daily_games_results = []

    for game in games_summary:
        game_result = dict()
        game_result['winner'] = game.find(class_='winner').find('a').get_text()
        game_result['winner_score'] = game.find(class_='winner').find(class_='right').get_text()
        game_result['loser'] = game.find(class_='loser').find('a').get_text()
        game_result['loser_score'] = game.find(class_='loser').find(class_='right').get_text()
        daily_games_results.append(game_result)

    return daily_games_results


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


def add_schedule_to_db(game, cursor):
    cursor.execute("INSERT INTO public.games_list(game_date, away_team, away_team_score, "
                   "home_team, home_team_score, overtime, attendance, game_id)"
                   "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                   (game.game_date, game.away_team, game.away_team_score, game.home_team,
                    game.home_team_score, game.overtime, game.attendance, game.game_id))


def parse_schedule_data(schedule, cursor):
    games_list = schedule.find_all('tr')
    for game in games_list:
        game_object = ScheduleGame(game)
        add_schedule_to_db(game_object, cursor)


def get_games_from_db(start_date, end_date=None):
    """
    Retrieves game data for the specified time range
    :param cursor: database cursor object
    :param start_date: datetime object representing the start date of the query
    :param end_date:  datetime object representing the end date of the query
    :return: a list of Game objects
    """

    if end_date is None:
        return GamesList.objects.filter(game_date=start_date)
    #else:
    #    cursor.execute("SELECT * FROM public.games_list WHERE game_date >= %s AND game_date <= %s",
    #                   (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))



def update_scores_in_db(cursor, start_date, end_date=None):
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
        cursor.execute("UPDATE public.games_list "
                       "SET away_team_score = %s, home_team_score = %s, overtime = %s, attendance = %s"
                       "WHERE game_id=%s;",
                       (int(game.away_team_score), int(game.home_team_score), game.overtime, int(game.attendance),
                        game.game_id))
    conn.commit()
    return None


def get_daily_games_list(cursor, date):
    cursor.execute("SELECT game_date, away_team, home_team, game_id FROM public.games_list WHERE game_date = %s",
                   (datetime.datetime.strptime(date, '%Y-%m-%d'),))
    games_list = []
    for game in cursor.fetchall():
        games_list.append(Game(game_date=game[0], away_team=game[1], home_team=game[2], game_id=game[3]))

    return games_list


