import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import login as log_in, logout, authenticate
from django.contrib import messages
from django.contrib.auth.views import login
from rest_framework.views import APIView
from ceat.settings import CATEGORY_DICT
from .forms import UserCreationForm
from .models import User


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
                url = '{}/api/users/{}'.format(MY_URL, user.id)
                response = requests.get(url)
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
        Returns restaurant recommendation based on anonymous user's given term
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


def register(request):
    if request.user.is_authenticated:
         return HttpResponseRedirect(reverse('recommender:home'))
    elif request.method == 'POST':
        form = UserCreationForm(data=request.POST)

        if request.POST['username'] != '' and request.POST['password1'] != '' and request.POST['password2'] != '':
            if len(request.POST['username']) < 8:
                messages.error(request, 'Username should be at least 8 characters')
            elif len(request.POST['username']) > 16:
                messages.error(request, 'Username can only be up to 16 characters')
            elif form.is_valid():
                new_user = form.save(commit=False)
                new_user.first_name = request.POST['first_name'].title()
                new_user.last_name = request.POST['last_name'].title()
                new_user.save()
                authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
                log_in(request, authenticated_user)
                return HttpResponseRedirect(reverse('users:start_prefs'))
        else:
            messages.error(request, 'You left one or more required field(s) blank')
            
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)


def custom_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('recommender:home'))     
    else:
        return login(request, template_name='users/login.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    
    return HttpResponseRedirect(reverse('recommender:home'))


def prefs_view(request):
    if request.user.is_authenticated:
        print(request.META.get('HTTP_REFERER'))
        return render(request, template_name='users/start_prefs.html', context={'categories': CATEGORY_DICT})
    
    return HttpResponseRedirect(reverse('recommender:home'))


def settings_prefs(request):
    user_prefs = eval(User.objects.get(pk=request.user.id).preferences)
    if request.user.is_authenticated:
        return render(request, template_name='users/settings_prefs.html', context={'categories': CATEGORY_DICT, 'preferences': user_prefs})
    
    return HttpResponseRedirect(reverse('recommender:home'))
