from django.contrib import admin
from django.urls import path

from django.urls import path
from .import views

app_name = 'music'
urlpatterns = [
	path('http://127.0.0.1:8000/music/', views.ShowEvents, name = 'index'),
	path('http://127.0.0.1:8000/music/search', views.QueryEvents, name = 'detail'),
]

