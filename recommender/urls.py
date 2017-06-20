from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<keyword>[\w\-@.+_]+)/$', views.soloRecommendation, name='solorec'),
]
