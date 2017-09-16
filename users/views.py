import json
from django.shortcuts import render, redirect
from django.dispatch import receiver
from django.core import serializers
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added, social_account_removed
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_auth.registration.views import SocialLoginView
from ceat.settings import CATEGORY_DICT, MY_URL
from .models import User, History, Group


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


@receiver(user_signed_up)
def social_profilepic(user, **kwargs):
    socialaccount = SocialAccount.objects.filter(user=user)
    if socialaccount:
        picture_url = "http://graph.facebook.com/{0}/picture?width={1}&height={1}".format(socialaccount[0].uid, 256)
        user.avatar_url = picture_url
        user.save()


@receiver(social_account_added)
def social_namepic_set(sociallogin, **kwargs):
    user = sociallogin.account.user
    user_socialAcc_count = SocialAccount.objects.filter(user=user).count()
    if user_socialAcc_count == 1:
        picture_url = "http://graph.facebook.com/{0}/picture?width={1}&height={1}".format(sociallogin.account.uid, 256)
        user.avatar_url = picture_url
        user.first_name = sociallogin.account.extra_data['first_name']
        user.last_name = sociallogin.account.extra_data['last_name']
        user.save()


@receiver(social_account_removed)
def social_namepic_remove(socialaccount, **kwargs):
    user = socialaccount.user
    user_socialAcc_count = SocialAccount.objects.filter(user=user).count()
    if user_socialAcc_count == 0:
        user.avatar_url = None
        user.first_name = ''
        user.last_name = ''
        user.save()


class setPreferences(APIView):
    """
    Set Preferences Endpoint
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        """
        Sets user preferences, then returns the changes
        """
        try:
            uid = int(self.request.data.get('uid'))
            ratings = json.loads(self.request.data.get('ratings'))
        except Exception as ex:
            return HttpResponse(json.dumps({'error': 'Error! Invalid parameters!'}), content_type="application/json")

        user = User.objects.get(pk=uid)
        user_prefs = eval(user.preferences)
        for category in ratings:
            user_prefs[category] = ratings[category]
        user.preferences = json.dumps(user_prefs)
        user.save()
        return HttpResponse(json.dumps({'uid': uid, 'ratings': ratings}), content_type="application/json")


class addGroup(APIView):
    """
    Add Group Endpoint
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        """
        Creates new group, then returns the details
        """
        try:
            uid = int(self.request.data.get('uid'))
            members = eval(self.request.data.get('members'))
            name = self.request.data.get('name')
        except Exception as ex:
            return HttpResponse(json.dumps({'error': 'Error! Invalid parameters!'}), content_type="application/json")

        user = User.objects.get(pk=uid)
        groupMembers = User.objects.filter(pk__in=members)
        newGroup = Group.objects.create(creator=user, name=name)
        newGroup.members = groupMembers
        newGroup.save()
        return HttpResponse(json.dumps({'uid': uid, 'name': name, 'members': members}), content_type="application/json")


class setHistory(APIView):
    """
    Set History Endpoint
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        """
        Rates user history, then returns the changes
        """
        try:
            uid = int(self.request.data.get('uid'))
            ratings = json.loads(self.request.data.get('ratings'))
        except Exception as ex:
            return HttpResponse(json.dumps({'error': 'Error! Invalid parameters!'}), content_type="application/json")

        user = User.objects.get(pk=uid)
        user_prefs = eval(user.preferences)
        historyIds = []
        for history in ratings:
            historyIds.append(int(history))
        ratedHistories = History.objects.filter(pk__in=historyIds)
        for history in ratedHistories:
            restoCats = eval(history.categories)
            if ratings[str(history.id)] == 1:
                history.isLiked = True
                for category in restoCats:
                    user_prefs[category] = 1
            else:
                history.isLiked = False
                for category in restoCats:
                    user_prefs[category] = -1

            history.save()
        user.preferences = json.dumps(user_prefs)
        user.save()
        return HttpResponse(json.dumps({'uid': uid, 'ratings': ratings}), content_type="application/json")


class addHistory(APIView):
    """
    Add History Endpoint
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        """
        Adds to user history, then returns the changes
        """
        try:
            resto = self.request.data.get('resto')
            uid = int(self.request.data.get('uid'))
            categories = self.request.data.get('categories')
        except Exception as ex:
            print(ex)
            return HttpResponse(json.dumps({'error': 'Error! Invalid parameters!'}), content_type="application/json")

        user = User.objects.get(pk=uid)
        newHistory = History.objects.create(user=user, resto=resto, categories=categories)
        newHistory.save()
        newHistory = History.objects.last()

        return HttpResponse(json.dumps({'user': newHistory.user.id, 'resto': newHistory.resto}), content_type="application/json")


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


def account_profile(request):
    if request.user.is_authenticated:            
        user_prefs = eval(request.user.preferences)
        userHistory = History.objects.filter(user=request.user, isLiked__isnull=True)
        userHistoryRated = History.objects.filter(user=request.user, isLiked__isnull=False)

        context = {'categories': CATEGORY_DICT, 'preferences': user_prefs, 'histories': userHistory, 'ratedHistories': userHistoryRated}

        user_social = SocialAccount.objects.filter(user=request.user).count()
        if user_social:
            user_friends_temp = SocialAccount.objects.get(user=request.user).extra_data['friends']['data']
            user_friends = []
            for person in user_friends_temp:
                if person['name'] in ('Andre Arbitrario'):
                    continue
                socialAcc = SocialAccount.objects.get(uid=person['id'])
                person['picture'] = socialAcc.extra_data['picture']['data']['url']
                person['id'] = socialAcc.user.id
                user_friends.append(person)
            context['friends'] = user_friends
        user_created_groups = Group.objects.filter(creator=request.user)
        if user_created_groups:
            user_groups = []
            for group in user_created_groups:
                groupEntry = dict()
                groupEntry['id'] = group.id
                groupEntry['name'] = group.name
                groupEntry['members'] = []
                groupEntryMembers = group.members.all()
                for member in groupEntryMembers:
                    memberDetails = dict()
                    memberDetails['id'] = member.id
                    memberDetails['name'] = member.get_full_name()
                    groupEntry['members'].append(memberDetails)
                user_groups.append(groupEntry)
            context['groups'] = user_groups

        return render(request, template_name='account/profile.html', context=context)
    return redirect(reverse('account_login')+'?next=/accounts/preferences/')
