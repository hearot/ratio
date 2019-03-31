from django.urls import path

from .views import competitions

app_name = 'competition'

urlpatterns = [
    path('competitions', competitions, name='competitions_default'),
    path('competitions/<int:page>', competitions, name='competitions')
]
