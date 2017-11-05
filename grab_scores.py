import requests
import database
from bs4 import BeautifulSoup
from game import Game

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
    html = get_html(url)
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
        game_object = Game(game)
        add_schedule_to_db(game_object, cursor)


conn = database.db_connect()
cursor = conn.cursor()

schedule = get_schedule()
parse_schedule_data(schedule, cursor)
conn.commit()
conn.close()
