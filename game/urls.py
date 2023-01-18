from django.urls import path

from . import views

app_name = 'game'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:game_id>/', views.start, name='start'),
    path('<int:game_id>/<int:player_id>/<int:question_id>/', views.detail, name='detail'),
    path('<int:game_id>/<int:player_id>/results/', views.results, name='results'),
    path('<int:game_id>/<int:player_id>/next_question/', views.next_question, name='next_question'),
    path('<int:game_id>/<int:player_id>/<int:question_id>/answer/', views.answer, name='answer'),
]
