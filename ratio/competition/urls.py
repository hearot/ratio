from django.urls import path

from .views import (answer, api_leaderboard, CompetitionView,
                    competitions, join_competition, WatchCompetitionView)

app_name = 'competition'

urlpatterns = [
    path('api/competition/<int:pk>/leaderboard', api_leaderboard, name='api_leaderboard'),
    path('answer/<int:pk>', answer, name='answer'),
    path('competition/description/<int:pk>', CompetitionView.as_view(), name='competition_description'),
    path('competitions', competitions, name='competitions_default'),
    path('competitions/<int:page>', competitions, name='competitions'),
    path('join/<int:pk>', join_competition, name="join_competition"),
    path('watch/<int:pk>', WatchCompetitionView.as_view(), name="watch_competition")
]
