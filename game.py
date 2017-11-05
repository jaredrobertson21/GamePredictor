class Game:
    """
    Game objects encapsulate all data about past and upcoming games
    """
    def __init__(self, game_information):
        self.game_date = game_information.find('th').get_text()
        self.away_team = game_information.find('td', {'data-stat': 'visitor_team_name'}).get_text()
        self.home_team = game_information.find('td', {'data-stat': 'home_team_name'}).get_text()
        self.game_id = game_information.th.attrs.get('csk')

        if game_information.find('td', {'data-stat': 'visitor_goals'}).get_text() == '':
            self.away_team_score = None
            self.home_team_score = None
            self.overtime = None
            self.attendance = None
        else:
            self.away_team_score = game_information.find('td', {'data-stat': 'visitor_goals'}).get_text()
            self.home_team_score = game_information.find('td', {'data-stat': 'home_goals'}).get_text()
            self.overtime = game_information.find('td', {'data-stat': 'overtimes'}).get_text()
            self.attendance = game_information.find('td', {'data-stat': 'attendance'}).get_text().replace(',', '')


    def parse_game_id(self, game_information):
        """
        The game_id is scraped in the form of <a href="/boxscores/game_id.html"> at the start of the game object
        This function strips out the game_id from the link text.
        :param game: BS4 tag object
        :return: string containing the game_id
        """
        return game_information.find('a')['href'].split('/')[2].split('.')[0]

    def __repr__(self):
        return "Date: {}\t{} @ {}".format(self.game_date, self.away_team, self.home_team)
