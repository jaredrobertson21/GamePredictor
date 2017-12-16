"""
Run this script to update the TeamStats model with the latest statistics for each team.
Specify the date(s) to be updated in the __main__ function.
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamepredictor.settings')

import django
django.setup()

from games.models import GamesList, TeamStats