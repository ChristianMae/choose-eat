import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import login as log_in, logout, authenticate
from django.contrib import messages
from django.contrib.auth.views import login
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from ceat.settings import CATEGORY_DICT
from .forms import UserCreationForm
from .models import User


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
            elif form.is_valid():
                new_user = form.save(commit=False)
                new_user.first_name = request.POST['first_name'].title()
                new_user.last_name = request.POST['last_name'].title()
                new_user.save()
                authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
                log_in(request, authenticated_user)
                return HttpResponseRedirect(reverse('recommender:home'))
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
        return render(request, template_name='users/set_prefs.html', context={'categories': CATEGORY_DICT})
    
    return HttpResponseRedirect(reverse('recommender:home'))
