from django.urls import path

from . import views

app_name = 'fractal'
urlpatterns = [
    path('', views.index, name='index'),
    path('sierpinski/', views.sierpinski, name='sierpinski'),
]

