from django.urls import path

from . import views

urlpatterns = [
    path('youtubesearch/', views.YouTubeSearch, name='youtubesearch'),

]