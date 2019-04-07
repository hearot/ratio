from django.urls import path

from .views import (answer, api_leaderboard, CompetitionView,
                    competitions, join_competition, questions, WatchCompetitionView)

app_name = 'competition'

urlpatterns = [
    path('api/competition/<int:pk>/leaderboard', api_leaderboard, name='api_leaderboard'),
    path('competition/answer/<int:pk>', answer, name='answer'),
    path('competition/description/<int:pk>', CompetitionView.as_view(), name='competition_description'),
    path('competition/join/<int:pk>', join_competition, name="join_competition"),
    path('competition/questions/<int:pk>', questions, name="questions"),
    path('competitions/watch/<int:pk>', WatchCompetitionView.as_view(), name="watch_competition"),
    path('competitions', competitions, name='competitions_default'),
    path('competitions/<int:page>', competitions, name='competitions')
]
