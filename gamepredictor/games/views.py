import datetime
from django.shortcuts import render
from .grab_scores import get_games_from_db


def home(request):
    today = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
    games = get_games_from_db(today)
    return render(request, 'games/home.html', {'games_list': games, 'today': today})


def submit_prediction(request):
    today = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
    games = get_games_from_db(today)
    return render(request, 'games/home.html', {'games_list': games, 'today': today})

    #
    # <!--<form id="{{ game.away_team }}{{ game.game_id }}" method="POST" action="{% url 'submit_prediction' game.game_id %}">-->
    #     <!--{% csrf_token %}-->
    #     <!--<input type="hidden">-->
    # <!--</form>-->
    # <!--<form id="{{ game.home_team }}{{ game.game_id }}" method="POST" action="{% url 'submit_prediction' game.game_id %}">-->
    #     <!--{% csrf_token %}-->
    #     <!--<input type="hidden">-->
    # <!--</form>-->