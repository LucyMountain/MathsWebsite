from django.urls import path

from . import views

app_name = 'game'
urlpatterns = [
    path('', views.index, name='index'),
    path('game_engine/', views.game_engine, name='game_engine'),
    path('<int:game_id>/start/', views.start, name='start'),
]
