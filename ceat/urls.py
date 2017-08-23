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
from django.contrib import admin
from rest_framework import routers, serializers, viewsets
from rest_framework_swagger.views import get_swagger_view
from recommender.views import soloRecommendation, groupRecommendation, trialRecommendation
from users.views import setPreferences, login, registration
from users.models import User, Group


# Serializers define the API representation.
# User Serializer
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email', 'bio', 'birth_date', 'preferences', 'date_joined')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# User Serializer
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name', 'creator', 'members')

# ViewSets define the view behavior.
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

schema_view = get_swagger_view(title="Choose-Eat API")
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api-endpoints/', schema_view),
    url(r'^api/soloRecommendation', soloRecommendation.as_view(), name="soloRec"),
    url(r'^api/groupRecommendation', groupRecommendation.as_view(), name="groupRec"),
    url(r'^api/trialRecommendation', trialRecommendation.as_view(), name="trialRec"),
    url(r'^api/setPreferences', setPreferences.as_view(), name="setPrefs"),
    url(r'^api/login', login.as_view()),
    url(r'^api/registration', registration.as_view()),
    url(r'', include('recommender.urls', namespace='recommender')),
    url(r'', include('users.urls', namespace='users')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
