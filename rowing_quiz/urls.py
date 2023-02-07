from django.urls import path

from . import views

app_name = 'rowing_quiz'
urlpatterns = [
    path('', views.index, name='index'),
    path('quiz_engine/', views.quiz_engine, name='quiz_engine'),
    path('start/', views.start, name='start'),
]
