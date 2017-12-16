import datetime, json
from django.shortcuts import render, redirect
from .grab_scores import get_games_from_db
from .models import GamePredictions, TeamStats


def home(request):
    today = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
    games = get_games_from_db(today)
    games_data = []
    team_stats_raw = TeamStats.objects.all()
    team_stats = {}

    # refactor these into other modules
    for team in team_stats_raw:
        team_stats[team.team] = {
            'wins': team.wins,
            'losses': team.losses,
            'otl': team.otl,
            'streak': team.streak,
            'logo': team.logo,
        }

    for game in games:
        away_team = game.away_team
        home_team = game.home_team
        games_data.append({
            'game_date': game.game_date,
            'away_team': game.away_team,
            'away_team_score': game.away_team_score,
            'home_team': game.home_team,
            'home_team_score': game.home_team_score,
            'overtime': game.overtime,
            'attendance': game.attendance,
            'game_id': game.game_id,
            'away_team_wins': team_stats[away_team]['wins'],
            'away_team_losses': team_stats[away_team]['losses'],
            'away_team_otl': team_stats[away_team]['otl'],
            'away_team_logo': team_stats[away_team]['logo'],
            'home_team_wins': team_stats[home_team]['wins'],
            'home_team_losses': team_stats[home_team]['losses'],
            'home_team_otl': team_stats[home_team]['otl'],
            'home_team_logo': team_stats[home_team]['logo'],
        })

    return render(request, 'games/home.html', {'games_data': games_data, 'today': today})


def submit_data(request):
    if request.method == 'POST':
        submitted_data = json.loads(request.body.decode("utf-8"))
        for game in submitted_data:
            GamePredictions.objects.get_or_create(game_id=game,
                                                  prediction=submitted_data[game],
                                                  user_id_id=request.user.id,
                                                  game_date=datetime.datetime.strftime(datetime.datetime.today(),
                                                                                       '%Y-%m-%d'))
        return redirect('home')


