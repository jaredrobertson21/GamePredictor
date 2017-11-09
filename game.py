class Game:
    """
    Game objects encapsulate game data from the past or future
    """
    def __init__(self, game_information):
        self.game_date = game_information[1]
        self.away_team = game_information[2]
        self.away_team_score = game_information[3]
        self.home_team = game_information[4]
        self.home_team_score = game_information[5]
        self.game_id = game_information[6]
        self.overtime = game_information[7]
        self.attendance = game_information[8]

    def winner(self):
        if self.away_team_score > self.home_team_score:
            return self.away_team
        else:
            return self.home_team

    def loser(self):
        if self.away_team_score < self.home_team_score:
            return self.away_team
        else:
            return self.home_team

    # TODO: add exception handling for winner/loser methods for games that have not been played yet

    def __repr__(self):
        return "Game date: {}\t{} @ {}".format(self.game_date, self.away_team, self.home_team)


class ScheduleGame:
    """
    ScheduleGame objects encapsulate all game data for the purpose of parsing the game schedule.
    game_information is a BeautifulSoup tag object
    """
    def __init__(self, game_information):
        self.game_date = game_information.find('th').get_text()
        self.away_team = game_information.find('td', {'data-stat': 'visitor_team_name'}).get_text()
        self.home_team = game_information.find('td', {'data-stat': 'home_team_name'}).get_text()
        self.game_id = game_information.th.attrs.get('csk')

        if game_information.find('td', {'data-stat': 'visitor_goals'}).get_text() == '':
            # These fields must be sent to the database as None if the game has not happened yet
            self.away_team_score = None
            self.home_team_score = None
            self.overtime = None
            self.attendance = None
        else:
            self.away_team_score = game_information.find('td', {'data-stat': 'visitor_goals'}).get_text()
            self.home_team_score = game_information.find('td', {'data-stat': 'home_goals'}).get_text()
            self.overtime = game_information.find('td', {'data-stat': 'overtimes'}).get_text()
            self.attendance = game_information.find('td', {'data-stat': 'attendance'}).get_text().replace(',', '')

    def __repr__(self):
        return "Date: {}\t{} @ {}".format(self.game_date, self.away_team, self.home_team)