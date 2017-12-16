from django.shortcuts import render
from games.models import UserStats


def stats(request):
    user_record = UserStats.objects.get(id=request.user.id)
    return render(request, 'stats/stats.html', {'user_record': user_record})
