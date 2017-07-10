from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from random import shuffle
import json
import os
from .utils import query_api
from ceat.settings import CATEGORY_DICT, BASE_DIR
from users.models import UserGroup
import time


def soloRecommendation(request, user=1, latitude=7.0689124, longitude=125.6018725, term=None):
	start_time = time.time()
	#allRestaurants = query_api(longitude, latitude)['businesses']
	allRestaurants = [x['name'] for x in query_api(longitude, latitude)['businesses']]
	forUser = User.objects.get(pk=user)
	user_prefs = eval(forUser.profile.preferences)
	user_dislikes = [x for x in user_prefs if user_prefs[x] == -1]
	categoryDislikes = []
	for category in user_dislikes:
		categoryDislikes.append(CATEGORY_DICT[category])
	categoryDislikeString = ','.join(categoryDislikes)
	print('Dislikes: {}'.format(categoryDislikeString))
	#dislikes = query_api(longitude, latitude, categories=categoryDislikeString)['businesses'] if categoryDislikeString else []
	dislikes = [x['name'] for x in query_api(longitude, latitude, categories=categoryDislikeString)['businesses']] if categoryDislikeString else []
	if term:
		# Give recommendations using keyword
		#likes = query_api(longitude, latitude, term)['businesses']
		likes = [x['name'] for x in query_api(longitude, latitude, term)['businesses']]
		print('Search term: {}'.format(term))	
	else:
		# Give recommendations based on user preferences
		user_likes = [x for x in user_prefs if user_prefs[x] == 1]
		categoryLikes = []
		for category in user_likes:
			categoryLikes.append(CATEGORY_DICT[category])
		categoryLikeString = ','.join(categoryLikes)
		print('Likes: {}'.format(categoryLikeString))
		#likes = query_api(longitude, latitude, categories=categoryLikeString)['businesses']
		likes = [x['name'] for x in query_api(longitude, latitude, categories=categoryLikeString)['businesses']]
	dislikes = set(dislikes)
	dislikes = list(dislikes)
	semilikes = [x for x in dislikes if x in likes]
	for item in semilikes:
		likes.remove(item)
	others = [x for x in allRestaurants if x not in likes+semilikes+dislikes]
	dislikes = [x for x in dislikes if x not in semilikes]
	shuffle(likes)
	shuffle(semilikes)
	shuffle(others)
	print("--- %s seconds ---" % (time.time() - start_time))
	return HttpResponse(json.dumps({'likes': likes, 'semilikes': semilikes, 'others': others, 'dislikes': dislikes}), content_type="application/json")
	

def groupRecommendation(request, userList={1,4}, groupList=[1], latitude=7.0689124, longitude=125.6018725, term=None):
	start_time = time.time()
	#allRestaurants = query_api(longitude, latitude)['businesses']
	allRestaurants = [x['name'] for x in query_api(longitude, latitude)['businesses']]
	for group in groupList:
		usersInGroup = UserGroup.objects.get(pk=group).profile_set.all()
		for user in usersInGroup:
			userList.add(int(user))

	userList = User.objects.filter(pk__in=userList)
	categoryDislikes = set()
	for user in userList:
		user_prefs = eval(user.profile.preferences)
		user_dislikes = [x for x in user_prefs if user_prefs[x] == -1]
		
		for category in user_dislikes:
			categoryDislikes.add(CATEGORY_DICT[category])

	categoryDislikeString = ','.join(categoryDislikes)
	print('Dislikes: {}'.format(categoryDislikeString))
	#dislikes = query_api(longitude, latitude, categories=categoryDislikeString)['businesses'] if categoryDislikeString else []
	dislikes = [x['name'] for x in query_api(longitude, latitude, categories=categoryDislikeString)['businesses']] if categoryDislikeString else []
	if term:
		# Give recommendations using keyword
		#likes = query_api(longitude, latitude, term)['businesses']
		likes = [x['name'] for x in query_api(longitude, latitude, term)['businesses']]
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
	dislikes = set(dislikes)
	dislikes = list(dislikes)
	semilikes = [x for x in dislikes if x in likes]
	for item in semilikes:
		likes.remove(item)
	others = [x for x in allRestaurants if x not in likes+semilikes+dislikes]
	dislikes = [x for x in dislikes if x not in semilikes]
	shuffle(likes)
	shuffle(semilikes)
	shuffle(others)
	print("--- %s seconds ---" % (time.time() - start_time))
	return HttpResponse(json.dumps({'likes': likes, 'semilikes': semilikes, 'others': others, 'dislikes': dislikes}), content_type="application/json")

"""
Missing:
- Consider price levels and location range
- Follow DRY (Probably combine both methods, but have a way to know if solo or group)
- Find out how to use URL Params for API Requests (remove hardcoded parameters)
- Deal with same name but different restaurants
"""