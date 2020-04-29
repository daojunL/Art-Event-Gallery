from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from music import views

urlpatterns = [
    path('detail/<int:pk>/', views.detail, name = 'detail'),
]
