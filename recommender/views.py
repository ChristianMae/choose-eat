from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from random import shuffle
import json
from .utils import query_api
from ceat.settings import CATEGORY_DICT


def soloRecommendation(request, user=1, latitude=7.0689124,  longitude=125.6018725, term=None):
	allRestaurants = query_api(longitude, latitude)['businesses']
	forUser = User.objects.get(pk=user)
	user_prefs = eval(forUser.profile.preferences)
	user_likes = [x for x in user_prefs if user_prefs[x] == 1]
	user_dislikes = [x for x in user_prefs if user_prefs[x] == -1]
	categoryLikes, categoryDislikes = [], []
	for category in user_likes:
		categoryLikes.append(CATEGORY_DICT[category])
	for category in user_dislikes:
		categoryDislikes.append(CATEGORY_DICT[category])
	categoryLikeString, categoryDislikeString = ','.join(categoryLikes), ','.join(categoryDislikes)
	print(categoryLikeString)
	print(categoryDislikeString)
	dislikes = query_api(longitude, latitude, categories=categoryDislikeString)['businesses']
	if term:
		# Give recommendations using keyword
		likes = query_api(longitude, latitude, term)['businesses']	
	else:
		# Give recommendations based on user preferences
		likes = query_api(longitude, latitude, categories=categoryLikeString)['businesses']
	semilikes = [x for x in dislikes if x in likes]
	for x in semilikes:
		likes.remove(x)
	others = [x for x in allRestaurants if x not in likes and x not in semilikes]
	shuffle(likes)
	shuffle(semilikes)
	shuffle(others)
	return HttpResponse(json.dumps({'likes': likes, 'semilikes': semilikes, 'others': others}), content_type="application/json")


def groupRecommendation(longitude, latitude, user, keyword=None):
	if keyword:
		# Searcch using keyword, longitude, latitude
		print("Hello")
	else:
		# Preferences
		print("Hello")
