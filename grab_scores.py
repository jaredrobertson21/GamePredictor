import requests
import database
from bs4 import BeautifulSoup
from game import ScheduleGame, Game
import datetime

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


def get_schedule():
    html = get_html(schedule_url)
    full_schedule = html.find('tbody')
    return full_schedule


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


def get_upcoming_games(cursor, start_date, end_date=None):
    """
    :param cursor: database cursor object
    :param start_date: datetime object representing the start date of the query
    :param end_date:  datetime object representing the end date of the query
    :return: a list of Game objects
    """
    if end_date is None:
        cursor.execute("SELECT * FROM public.games_list WHERE game_date = %s", (start_date.strftime('%Y-%m-%d'),))
    else:
        cursor.execute("SELECT * FROM public.games_list WHERE game_date >= %s AND game_date <= %s",
                       (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))

    games_list = cursor.fetchall()
    games_objects = []
    for game in games_list:
        game = Game(game)
        games_objects.append(game)

    return games_objects

conn = database.db_connect()
cursor = conn.cursor()

today = datetime.datetime.today() - datetime.timedelta(days=1)
upcoming_games = get_upcoming_games(cursor, today)
for game in upcoming_games:
    print(game.winner())

conn.close()
