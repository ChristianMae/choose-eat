from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from random import shuffle
import json
from .utils import query_api
from ceat.settings import CATEGORY_DICT


def soloRecommendation(request, user=1, latitude=7.0689124, longitude=125.6018725, term=None):
	allRestaurants = query_api(longitude, latitude)['businesses']
	forUser = User.objects.get(pk=user)
	user_prefs = eval(forUser.profile.preferences)
	user_dislikes = [x for x in user_prefs if user_prefs[x] == -1]
	categoryDislikes = []
	for category in user_dislikes:
		categoryDislikes.append(CATEGORY_DICT[category])
	categoryDislikeString = ','.join(categoryDislikes)
	print('Dislikes: {}'.format(categoryDislikeString))
	dislikes = query_api(longitude, latitude, categories=categoryDislikeString)['businesses'] if categoryDislikeString else []
	if term:
		# Give recommendations using keyword
		likes = query_api(longitude, latitude, term)['businesses']
		print('Search term: {}'.format(term))	
	else:
		# Give recommendations based on user preferences
		user_likes = [x for x in user_prefs if user_prefs[x] == 1]
		categoryLikes = []
		for category in user_likes:
			categoryLikes.append(CATEGORY_DICT[category])
		categoryLikeString = ','.join(categoryLikes)
		print('Likes: {}'.format(categoryLikeString))
		likes = query_api(longitude, latitude, categories=categoryLikeString)['businesses']
	semilikes = [x for x in dislikes if x in likes]
	for x in semilikes:
		likes.remove(x)
	others = [x for x in allRestaurants if x not in likes and x not in semilikes]
	dislikes = [x for x in dislikes if x not in semilikes]
	shuffle(likes)
	shuffle(semilikes)
	shuffle(others)
	return HttpResponse(json.dumps({'likes': likes, 'semilikes': semilikes, 'others': others, 'dislikes': dislikes}), content_type="application/json")


def groupRecommendation(longitude, latitude, user, keyword=None):
	allRestaurants = query_api(longitude, latitude)['businesses']
	#forUser = User.objects.get(pk=user) - Get all involved users here (including group)
	"""
	- Loop this part for all involved users
	- For every disliked category, add it in categoryDislikes (if it isn't in there yet)
	- Join all items in categoryDislikes list into categoryDislikeString afterwards

	user_prefs = eval(forUser.profile.preferences)
	user_dislikes = [x for x in user_prefs if user_prefs[x] == -1]
	categoryDislikes = []
	for category in user_dislikes:
		categoryDislikes.append(CATEGORY_DICT[category])
	"""
	#categoryDislikeString = ','.join(categoryDislikes)
	#print('Dislikes: {}'.format(categoryDislikeString))
	#dislikes = query_api(longitude, latitude, categories=categoryDislikeString)['businesses'] if categoryDislikeString else []
	if keyword:
		# Give recommendations using keyword
		likes = query_api(longitude, latitude, term)['businesses']
		print('Search term: {}'.format(term))
	else:
		# Give recommendations based on user preferences
		"""
		- Loop this part for all involved users
		- For every liked category, add it in categoryLikes (if it isn't in there yet)
		- Join all items in categoryLikes list into categoryLikeString afterwards

		user_likes = [x for x in user_prefs if user_prefs[x] == 1]
		categoryLikes = []
		for category in user_likes:
			categoryLikes.append(CATEGORY_DICT[category])
		"""
		categoryLikeString = ','.join(categoryLikes)
		print('Likes: {}'.format(categoryLikeString))
		likes = query_api(longitude, latitude, categories=categoryLikeString)['businesses']
	semilikes = [x for x in dislikes if x in likes]
	for x in semilikes:
		likes.remove(x)
	others = [x for x in allRestaurants if x not in likes and x not in semilikes]
	dislikes = [x for x in dislikes if x not in semilikes]
	shuffle(likes)
	shuffle(semilikes)
	shuffle(others)
	return HttpResponse(json.dumps({'likes': likes, 'semilikes': semilikes, 'others': others, 'dislikes': dislikes}), content_type="application/json")

"""
Missing:
- Consider price levels and location range
- Follow DRY (Probably combine both methods, but have a way to know if solo or group)
- Find out how to use URL Params for API Requests (remove hardcoded parameters)
"""