from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.views import login
from .forms import UserCreationForm


def register(request):
    if request.user.is_authenticated:
         return HttpResponseRedirect(reverse('recommender:home'))
    elif request.method == 'POST':
        form = UserCreationForm(data=request.POST)

        if request.POST['username'] != '' and request.POST['password1'] != '' and request.POST['password2'] != '':
            if len(request.POST['username']) < 8:
                messages.error(request, 'Username should be at least 8 characters')
            elif form.is_valid():
                new_user = form.save()
                authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
                login(request, authenticated_user)
                return HttpResponseRedirect(reverse('recommender:home'))
        else:
            messages.error(request, 'You left one or more field(s) blank')
            
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
        return render(request, 'users/logout.html')
    else:
        return HttpResponseRedirect(reverse('recommender:home'))
        