"""ceat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.auth.views import logout as logout_view
from django.contrib import admin
from rest_framework import routers, serializers, viewsets
from rest_framework_swagger.views import get_swagger_view
from recommender.views import soloRecommendation, groupRecommendation, trialRecommendation
from users.views import setPreferences, addHistory, setHistory, addGroup, FacebookLogin


schema_view = get_swagger_view(title="Choose-Eat API")
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-endpoints/', schema_view),
    url(r'^api/soloRecommendation', soloRecommendation.as_view(), name="soloRec"),
    url(r'^api/groupRecommendation', groupRecommendation.as_view(), name="groupRec"),
    url(r'^api/trialRecommendation', trialRecommendation.as_view(), name="trialRec"),
    url(r'^api/setPreferences', setPreferences.as_view(), name="setPrefs"),
    url(r'^api/setHistory', setHistory.as_view(), name="setHistory"),
    url(r'^api/addHistory', addHistory.as_view(), name="addHistory"),
    url(r'^api/addGroup', addGroup.as_view(), name="addGroup"),
    url(r'', include('recommender.urls', namespace='recommender')),
    url(r'', include('users.urls', namespace='users')),
    url(r'^accounts/logout/$', logout_view, {'next_page': '/'}),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
]
