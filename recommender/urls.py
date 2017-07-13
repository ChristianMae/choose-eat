from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^s/(?P<term>[\w\-@.+_]+)/$', views.soloRecommendation, name='solorec'),
    url(r'^s/$', views.soloRecommendation, name='solorec_key'),
    url(r'^g/(?P<term>[\w\-@.+_]+)/$', views.groupRecommendation, name='grprec'),
    url(r'^g/$', views.groupRecommendation, name='grprec_key'),
]
