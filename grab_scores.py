import requests
from bs4 import BeautifulSoup

url = 'https://hockey-reference.com'

# store game id as YYYYMMDD0HOM, where HOM is the first three letters of the home city

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

def get_upcoming_games():
    html = get_html(url)
    games_list = html.find_all('div', {"id": "games"})
    upcoming_games = []
    for game in games_list:
        game_list_links = game.find_all('a')
        individual_game = []
        for team in game_list_links:
            individual_game.append(team.get_text())
        print(individual_game)
        upcoming_games.append(individual_game)
    return upcoming_games
    # get home team
    # get away team

