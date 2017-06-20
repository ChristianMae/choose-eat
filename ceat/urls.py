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
from django.contrib.auth.models import User
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers, serializers, viewsets
from users.models import Profile


# Serializers define the API representation.
# User Serializer
class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'username', 'first_name', 'last_name', 'email')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Profile Serializer
class ProfileSerializer(serializers.HyperlinkedModelSerializer):
	user_details = UserSerializer(source='user')
	groups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

	class Meta:
		model = Profile
		fields = ('url', 'user_details', 'bio', 'birth_date', 'groups', 'preferences')

# ViewSets define the view behavior.
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^rec/', include('recommender.urls', namespace='recommender')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
