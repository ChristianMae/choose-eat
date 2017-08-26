import json
from django.shortcuts import render, redirect
from django.dispatch import receiver
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
from rest_framework.views import APIView
from ceat.settings import CATEGORY_DICT, MY_URL
from .models import User


@receiver(user_signed_up)
def social_profilepic(user, **kwargs):
    socialaccount = SocialAccount.objects.filter(user=user)
    if socialaccount:
        picture_url = "http://graph.facebook.com/{0}/picture?width={1}&height={1}".format(socialaccount[0].uid, 256)
        user.avatar_url = picture_url
        user.save()


class login(APIView):
    """
    Login Endpoint

    Parameters:
    username (string) - User's username
    password (string) - User's password
    """
    def get(self, request, format=None):
        """
        Returns user details if credentials are valid, else an error
        """
        username = self.request.query_params.get('username')
        password = self.request.query_params.get('password')
        
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                data = serializers.serialize('json', [user,])
                struct = json.loads(data)
                data = json.dumps(struct[0])

                response = data
            else:
                response = json.dumps({'error': 'Invalid password!'})
        except User.DoesNotExist:
            response = json.dumps({'error': 'User does not exist!'}) 
        
        return HttpResponse(response, content_type="application/json")


class registration(APIView):
    """
    Registration Endpoint

    Parameters:
    username (string) - User's username
    password (string) - User's password
    first_name (string) - User's first name
    last_name (string) - User's last name
    """
    def post(self, request, format=None):
        """
        Returns user details if credentials are valid, else an error
        """
        username = self.request.data.get('username')
        password = self.request.data.get('password')
        first_name = self.request.data.get('first_name')
        last_name = self.request.data.get('last_name')
        
        try:
            user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
            )

            user.set_password(validated_data['password'])
            user.save()

            data = serializers.serialize('json', [user,])
            struct = json.loads(data)
            data = json.dumps(struct[0])

            response = data
        except Exception as e:
            response = e if not hasattr(e, 'message') else e.message
        
        return HttpResponse(json.dumps({'error': response}))


class setPreferences(APIView):
    """
    Set Preferences Endpoint
    """
    def post(self, request, format=None):
        """
        Sets user preferences, then returns the changes
        """
        try:
            uid = int(self.request.data.get('uid'))
            ratings = json.loads(self.request.data.get('ratings'))
        except Exception as ex:
            print(ex)
            return HttpResponse(json.dumps({'error': 'Error! Invalid parameters!'}), content_type="application/json")

        user = User.objects.get(pk=uid)
        user_prefs = eval(user.preferences)
        for category in ratings:
            user_prefs[category] = ratings[category]
        user.preferences = json.dumps(user_prefs)
        user.save()
        return HttpResponse(json.dumps({'uid': uid, 'ratings': ratings}), content_type="application/json")


def startPrefs(request):
    if request.user.is_authenticated:
        user_prefs = eval(request.user.preferences)
        categories = {'Asian Fusion': 'asianfusion', 'Barbeque': 'bbq', 'Bistros': 'bistros', 'Cafes': 'cafes', 'Chicken': 'chickenshop', 'Chinese': 'chinese', 'Filipino': 'filipino', 'Italian': 'italian', 'Japanese': 'japanese', 'Korean': 'korean', 'Mexican': 'mexican', 'Noodles': 'noodles', 'Pizza': 'pizza', 'Seafood': 'seafood', 'Steakhouses': 'steak', 'Vegetarian': 'vegetarian'}
        for key, value in categories.items():
            if user_prefs[value] in (-1, 1):
                return HttpResponseRedirect(reverse('recommender:home'))
        else:
            return render(request, template_name='users/start_prefs.html', context={'categories': categories, 'MY_URL': MY_URL})
    return redirect(reverse('account_login')+'?next=/starting_preferences/')


def settings_prefs(request):
    if request.user.is_authenticated:
        user_prefs = eval(request.user.preferences)
        return render(request, template_name='users/settings_prefs.html', context={'categories': CATEGORY_DICT, 'preferences': user_prefs})
    return redirect(reverse('account_login')+'?next=/preferences/')
