import json
from random import shuffle
import requests
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from rest_framework.views import APIView
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
        except:
            return HttpResponse(json.dumps({'error': 'Error! Invalid parameters!'}), content_type="application/json")

        allRestaurants = [x for x in query_api(longitude, latitude, distance)['businesses']]
        user = User.objects.get(pk=uid)
        user_prefs = eval(user.preferences)
        user_dislikes = [x for x in user_prefs if user_prefs[x] == -1]
        categoryDislikeString = ','.join(user_dislikes)
        dislikes = query_api(longitude, latitude, distance, categories=categoryDislikeString)['businesses'] if categoryDislikeString else []
        if term:
        	# Give recommendations using keyword
        	likes = query_api(longitude, latitude, distance, term)['businesses']
        else:
        	# Give recommendations based on user preferences
            user_likes = [x for x in user_prefs if user_prefs[x] == 1]
            categoryLikeString = ','.join(user_likes)
            if categoryLikeString:
                likes = query_api(longitude, latitude, distance, categories=categoryLikeString)['businesses']
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
	        uid_list = set(eval(self.request.query_params.get('uid_list')))
	        gid_list = list(eval(self.request.query_params.get('gid_list')))
	        latitude = float(self.request.query_params.get('latitude'))
	        longitude = float(self.request.query_params.get('longitude'))
	        term = self.request.query_params.get('term')
        except:
        	return HttpResponse(json.dumps({'error': 'Error! Invalid parameters!'}), content_type="application/json")

        allRestaurants = query_api(longitude, latitude)['businesses']
        #allRestaurants = [x['name'] for x in query_api(longitude, latitude)['businesses']]
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
        	print('Dislikes: {}'.format(categoryDislikeString))
        	#dislikes = query_api(longitude, latitude, categories=categoryDislikeString)['businesses'] if categoryDislikeString else []
        	dislikes = [x['name'] for x in query_api(longitude, latitude, categories=categoryDislikeString)['businesses']] if categoryDislikeString else []
        	#likes = query_api(longitude, latitude, term)['businesses']
        	likes = [x['name'] for x in query_api(longitude, latitude, term)['businesses']]
        	print('Search term: {}'.format(term))
        	dislikes = set(dislikes)
        	dislikes = list(dislikes)
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
        	#dislikes = [x['name'] for x in query_api(longitude, latitude, categories=dislikeString)['businesses']] if dislikeString else []
        	dislikes = [x for x in query_api(longitude, latitude, categories=dislikeString)['businesses']] if dislikeString else []
        	#semilikes = [x['name'] for x in query_api(longitude, latitude, categories=semilikeString)['businesses']] if semilikeString else []
        	semilikes = [x for x in query_api(longitude, latitude, categories=semilikeString)['businesses']] if semilikeString else []
        	#likes = [x['name'] for x in query_api(longitude, latitude, categories=likeString)['businesses']]
        	likes = [x for x in query_api(longitude, latitude, categories=likeString)['businesses'] if x not in semilikes]

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

        allRestaurants = [x for x in query_api(longitude, latitude)['businesses']]
        likes = query_api(longitude, latitude, term=term)['businesses']
        others = [x for x in allRestaurants if x not in likes]
        return HttpResponse(json.dumps({'likes': likes, 'others': others}), content_type="application/json")

        
def home(request):
    template = 'recommender/home_in.html' if request.user.is_authenticated else 'recommender/home.html'
    context = {'googlekey': GOOGLE_API_KEY}

    return render(request, template, context)

"""
Missing:
- Consider price levels and location range
- Deal with same name but different restaurants
"""
