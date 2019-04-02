from django.urls import path

from .views import CompetitionView, competitions, join_competition

app_name = 'competition'

urlpatterns = [
    path('competition/description/<int:pk>', CompetitionView.as_view(), name='competition_description'),
    path('competitions', competitions, name='competitions_default'),
    path('competitions/<int:page>', competitions, name='competitions'),
    path('join/<int:pk>', join_competition, name="join_competition")
]
