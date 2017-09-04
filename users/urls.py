"""URLS for users app"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^starting_preferences/$', views.startPrefs, name='start_prefs'),
    url(r'^preferences/$', views.settings_prefs, name='settings_prefs'),
    url(r'^accounts/profile/$', views.account_profile, name='account_profile'),
]
