from django.urls import path

from . import views

app_name = 'sudoku'
urlpatterns = [
    path('', views.index, name='index'),
    path('solve/', views.solve, name='solve'),
    path('test/', views.test_example, name='test'),
]
