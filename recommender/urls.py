from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^rec/g/(?P<term>[\w\-@.+_]+)/$', views.groupRecommendation, name='grprec'),
    url(r'^rec/g/$', views.groupRecommendation, name='grprec_key'),
    url(r'^$', views.home, name='home')
]
