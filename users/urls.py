"""URLS for users app"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.custom_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout_view, name='logout'),
]