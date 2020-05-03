
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from dashboard import views as dashViews

urlpatterns = [
    path('detail/<int:pk>/', dashViews.detail, name='detail'),

]
