import requests
from bs4 import BeautifulSoup

url = 'https://hockey-reference.com'


def get_games_results():
    """
    Retrieves all games results from the previous day
    :return: a list of dictionaries with the keys: winner, winner_score, loser, loser_score
    """
    req = requests.get(url)
    html = BeautifulSoup(req.text, 'html.parser')
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

def get_upcoming_games():
    req = requests.get(url)
    html = BeautifulSoup(req.text, 'html.parser')
    games_list = html.find_all('div', {"id": "games"})