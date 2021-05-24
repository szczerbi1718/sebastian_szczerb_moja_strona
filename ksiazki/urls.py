from django.urls import path
from . import views

urlpatterns = [
    path('ksiazki/', views.ksiazkiviews, name='ksiazkiviews')
]