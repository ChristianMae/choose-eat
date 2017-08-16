from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^solo_recommendation/$', views.soloRec_page, name='solo'),
    url(r'^group_recommendation/$', views.groupRec_page, name='group'),
]
