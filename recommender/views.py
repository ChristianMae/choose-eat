import json
from random import shuffle
import requests
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from rest_framework.views import APIView
from allauth.socialaccount.models import SocialAccount
from users.models import User, Group
from ceat.settings import MY_URL, GOOGLE_API_KEY
from .utils import query_api


class soloRecommendation(APIView):
    """
    Solo Restaurant Recommendation Endpoint

    Parameters:
    uid (int) - User ID
    distance (int) - Distance the User is willing to travel
    latitude (double) - Latitude of User's current location
    longitude (double) - Longitude of User's current location
    term (string) - Optional search term
    """
    def get(self, request, format=None):
        """
        Returns restaurant recommendation based on user's preferences and location
        """
        try:
            uid = int(self.request.query_params.get('uid'))
            distance = int(self.request.query_params.get('distance'))
            latitude = float(self.request.query_params.get('latitude'))
            longitude = float(self.request.query_params.get('longitude'))
            term = self.request.query_params.get('term')
            price = self.request.query_params.get('price')
        except:
            return HttpResponse(json.dumps({'error': 'Error! Invalid parameters!'}), content_type="application/json")

        allRestaurants = query_api(longitude, latitude, distance, price=price)['businesses']
        user = User.objects.get(pk=uid)
        user_prefs = eval(user.preferences)
        user_dislikes = [x for x in user_prefs if user_prefs[x] == -1]
        categoryDislikeString = ','.join(user_dislikes)
        dislikes = query_api(longitude, latitude, distance, categories=categoryDislikeString, price=price)['businesses'] if categoryDislikeString else []
        if term:
        	# Give recommendations using keyword
            likes = query_api(longitude, latitude, distance, term, price=price)['businesses']
        else:
        	# Give recommendations based on user preferences
            user_likes = [x for x in user_prefs if user_prefs[x] == 1]
            categoryLikeString = ','.join(user_likes)
            if categoryLikeString:
                likes = query_api(longitude, latitude, distance, categories=categoryLikeString, price=price)['businesses']
            else:
                likes = []

        semilikes = [x for x in dislikes if x in likes]
        for item in semilikes:
        	likes.remove(item)
        others = [x for x in allRestaurants if x not in likes+semilikes+dislikes]
        dislikes = [x for x in dislikes if x not in semilikes]
        shuffle(likes)
        shuffle(semilikes)
        shuffle(others)
        return HttpResponse(json.dumps({'likes': likes, 'semilikes': semilikes, 'others': others, 'dislikes': dislikes}), content_type="application/json")


class groupRecommendation(APIView):
    """
    Group Restaurant Recommendation Endpoint

    Parameters:
    uid_list (set) - List of User IDs
    gid_list (list) - List of Groups
    latitude (double) - Latitude of User's current location
    longitude (double) - Longitude of User's current location
    term (string) - Optional search term
    """
    def get(self, request, format=None):
        """
        Returns restaurant recommendation based on group's preferences and location
        """
        try:
            uid_list = eval(self.request.query_params.get('uid_list'))
            gid_list = eval(self.request.query_params.get('gid_list'))
            distance = int(self.request.query_params.get('distance'))
            latitude = float(self.request.query_params.get('latitude'))
            longitude = float(self.request.query_params.get('longitude'))
            term = self.request.query_params.get('term')
            price = self.request.query_params.get('price')
        except:
        	return HttpResponse(json.dumps({'error': 'Error! Invalid parameters!'}), content_type="application/json")

        allRestaurants = query_api(longitude, latitude, distance, price=price)['businesses']
        for group in gid_list:
        	usersInGroup = Group.objects.get(pk=group).members.all()
        	for user in usersInGroup:
        		uid_list.add(int(user))

        uid_list = User.objects.filter(pk__in=uid_list)	
        if term:
        	# Give recommendations using keyword
        	categoryDislikes = set()
        	for user in uid_list:
        		user_prefs = eval(user.preferences)
        		user_dislikes = [x for x in user_prefs if user_prefs[x] == -1]
        		for category in user_dislikes:
        			categoryDislikes.add(category)

        	categoryDislikeString = ','.join(categoryDislikes)
        	dislikes = query_api(longitude, latitude, distance, categories=categoryDislikeString, price=price)['businesses'] if categoryDislikeString else []
        	likes = query_api(longitude, latitude, distance, term, price=price)['businesses']
        	semilikes = [x for x in dislikes if x in likes]
        	for item in semilikes:
        		likes.remove(item)
        	others = [x for x in allRestaurants if x not in likes+semilikes+dislikes]
        	dislikes = [x for x in dislikes if x not in semilikes]
        else:
        	# Give recommendations based on user preferences
        	prefScores = dict()
        	allDislikes, allLikes = set(), set()
        	for user in uid_list:
        		user_prefs = eval(user.preferences)
        		for pref in user_prefs:
        			if user_prefs[pref] == 1:
        				prefScores[pref] = prefScores[pref] + 1 if pref in prefScores else 1
        				allLikes.add(pref)
        			elif user_prefs[pref] == -1:
        				prefScores[pref] = prefScores[pref] - 1 if pref in prefScores else -1
        				allDislikes.add(pref)

        	user_likes = list()
        	user_semilikes = list()
        	user_dislikes = list()
        	for pref in prefScores:
        		score = prefScores[pref]
        		if score == len(uid_list):
        			user_likes.append(pref)
        		elif score > 0:
        			if pref in allDislikes:
        				user_semilikes.append(pref)
        			else:
        				user_likes.append(pref)
        		elif score < 0:
        			user_dislikes.append(pref)
        		else:
        			if pref in allLikes:
        				user_semilikes.append(pref)

        	likeString = ','.join(user_likes)
        	semilikeString = ','.join(user_semilikes)
        	dislikeString = ','.join(user_dislikes)
        	dislikes = query_api(longitude, latitude, distance, categories=dislikeString, price=price)['businesses'] if dislikeString else []
        	semilikes = query_api(longitude, latitude, distance, categories=semilikeString, price=price)['businesses'] if semilikeString else []
        	likes = [x for x in query_api(longitude, latitude, distance, categories=likeString, price=price)['businesses'] if x not in semilikes]

        	tempList = []
        	for item in dislikes:
        		if item in likes:
        			tempList.append(item)
        	for item in tempList:
        		likes.remove(item)
        		dislikes.remove(item)
        		if item not in semilikes:
        			semilikes.append(item)

        	others = [x for x in allRestaurants if x not in likes+semilikes+dislikes]
        shuffle(likes)
        shuffle(semilikes)
        shuffle(others)
        print('Likes: {}'.format(likeString))
        print('Dislikes: {}'.format(dislikeString))
        print('Semilikes: {}'.format(semilikeString))
        return HttpResponse(json.dumps({'likes': likes, 'semilikes': semilikes, 'others': others, 'dislikes': dislikes}), content_type="application/json")

        
class trialRecommendation(APIView):
    """
    Anonymous Restaurant Recommendation Endpoint

    Parameters:
    latitude (double) - Latitude of User's current location
    longitude (double) - Longitude of User's current location
    term (string) - Required search term
    """
    def get(self, request, format=None):
        """
        Returns restaurant recommendation based on anonymous user's given term
        """
        try:
            latitude = float(self.request.query_params.get('latitude'))
            longitude = float(self.request.query_params.get('longitude'))
            term = self.request.query_params.get('term')
        except:
            return HttpResponse(json.dumps({'error': 'Error! Invalid parameters!'}), content_type="application/json")

        allRestaurants = query_api(longitude, latitude)['businesses']
        likes = query_api(longitude, latitude, term=term)['businesses']
        others = [x for x in allRestaurants if x not in likes]
        return HttpResponse(json.dumps({'likes': likes, 'others': others}), content_type="application/json")

        
def home(request):
    template = 'recommender/home.html'
    context = {'googlekey': GOOGLE_API_KEY}

    if request.user.is_authenticated:
        template = 'recommender/home_in.html'
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
                    memberDetails['picture'] = member.avatar_url
                    groupEntry['members'].append(memberDetails)
                user_groups.append(groupEntry)
            context['groups'] = user_groups

    return render(request, template, context)

"""
Missing:
- Consider price levels and location range
- Deal with same name but different restaurants
"""
