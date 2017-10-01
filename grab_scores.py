import requests
from bs4 import BeautifulSoup

url = 'https://baseball-reference.com'
req = requests.get(url)
html = BeautifulSoup(req.text, 'html.parser')

games_summary = html.find_all(class_='game_summary')

for game in games_summary:
	if game.a:
		print game.text.strip()
