from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<term>[\w\-@.+_]+)/$', views.soloRecommendation, name='solorec'),
    url(r'^$', views.soloRecommendation, name='solorec_key'),
]
