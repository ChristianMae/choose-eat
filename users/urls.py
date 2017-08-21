"""URLS for users app"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.custom_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^starting_preferences/$', views.prefs_view, name='start_prefs'),
    url(r'^preferences/$', views.settings_prefs, name='settings_prefs'),
]
