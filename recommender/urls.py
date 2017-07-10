from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<term>[\w\-@.+_]+)/$', views.soloRecommendation, name='solorec'),
    url(r'^$', views.soloRecommendation, name='solorec_key'),
    url(r'^g/(?P<term>[\w\-@.+_]+)/$', views.groupRecommendation, name='grprec'),
    url(r'^g/$', views.groupRecommendation, name='grprec_key'),
]
