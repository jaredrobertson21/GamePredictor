class Game:
    """
    Game objects encapsulate game data from the past or future
    """
    def __init__(self, game_date=None, away_team=None, away_team_score=None, home_team=None, home_team_score=None,
                 game_id=None, overtime=None, attendance=None):
        self.game_date = game_date
        self.away_team = away_team
        self.away_team_score = away_team_score
        self.home_team = home_team
        self.home_team_score = home_team_score
        self.game_id = game_id
        self.overtime = overtime
        self.attendance = attendance

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

    def winner(self):
        if self.away_team_score:
            if self.away_team_score > self.home_team_score:
                return self.away_team
            else:
                return self.home_team
        return "Game has not yet been played"

    def loser(self):
        if self.away_team_score:
            if self.away_team_score > self.home_team_score:
                return self.home_team
            else:
                return self.away_team
        return "Game has not yet been played"

    def is_overtime(self):
        if self.overtime != '':
            return True
        return False