# Ratio: Quisque faber fortunae suae.
# Copyright (C) 2019 Hearot
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
