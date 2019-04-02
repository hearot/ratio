from django.urls import path

from .views import CompetitionView, competitions

app_name = 'competition'

urlpatterns = [
    path('competition/description/<int:pk>', CompetitionView.as_view(), name='competition_description'),
    path('competitions', competitions, name='competitions_default'),
    path('competitions/<int:page>', competitions, name='competitions')
]
