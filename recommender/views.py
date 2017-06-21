from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
import json
from .utils import query_api
from ceat.settings import CATEGORY_DICT


# Create your views here.
def soloRecommendation(request, user=1, latitude=7.0689124,  longitude=125.6018725, term=None):
	allRestaurants = query_api(longitude, latitude)['businesses']
	if term:
		# Search using keyword, longitude, latitude
		likes = query_api(longitude, latitude, term)['businesses']	
	else:
		# Preferences
		forUser = User.objects.get(pk=user)
		user_prefs = eval(forUser.profile.preferences)
		user_likes = [x for x in user_prefs if user_prefs[x]]
		# look into using dislikes too
		categoryString = ''
		for category in user_likes:
			categoryString = '{}{},'.format(categoryString, CATEGORY_DICT[category])
		categoryString = categoryString[:-1]
		likes = query_api(longitude, latitude, categories=categoryString)['businesses']
	others = [x for x in allRestaurants if x not in likes]
	return HttpResponse(json.dumps({'related': likes, 'others': others}), content_type="application/json")


def groupRecommendation(longitude, latitude, user, keyword=None):
	if keyword:
		# Searcch using keyword, longitude, latitude
		print("Hello")

	else:
		# Preferences
		print("Hello")
