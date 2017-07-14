import json
import time
from random import shuffle
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import Group
from users.models import User
from ceat.settings import CATEGORY_DICT
from .utils import query_api


def soloRecommendation(request, user=1, latitude=7.0689124, longitude=125.6018725, term=None):
	start_time = time.time()
	#allRestaurants = query_api(longitude, latitude)['businesses']
	allRestaurants = [x['name'] for x in query_api(longitude, latitude)['businesses']]
	forUser = User.objects.get(pk=user)
	user_prefs = eval(forUser.preferences)
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
		usersInGroup = Group.objects.get(pk=group).user_set.all()
		for user in usersInGroup:
			userList.add(int(user))

	userList = User.objects.filter(pk__in=userList)	
	if term:
		# Give recommendations using keyword
		categoryDislikes = set()
		for user in userList:
			user_prefs = eval(user.preferences)
			user_dislikes = [x for x in user_prefs if user_prefs[x] == -1]
			for category in user_dislikes:
				categoryDislikes.add(CATEGORY_DICT[category])

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
		for user in userList:
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
			if score == len(userList):
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
		
		likeString = ','.join([CATEGORY_DICT[category] for category in user_likes])
		semilikeString = ','.join([CATEGORY_DICT[category] for category in user_semilikes])
		dislikeString = ','.join([CATEGORY_DICT[category] for category in user_dislikes])
		print('Likes: {}'.format(likeString))
		print('Semi-likes: {}'.format(semilikeString))
		print('Dislikes: {}'.format(dislikeString))
		semilikes = [x['name'] for x in query_api(longitude, latitude, categories=semilikeString)['businesses']]
		likes = [x['name'] for x in query_api(longitude, latitude, categories=likeString)['businesses'] if x['name'] not in semilikes]
		dislikes = [x['name'] for x in query_api(longitude, latitude, categories=dislikeString)['businesses'] if x['name'] not in likes+semilikes]
		others = [x for x in allRestaurants if x not in likes+semilikes+dislikes]
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