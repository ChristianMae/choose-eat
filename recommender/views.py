from django.http import HttpResponse
from django.shortcuts import render
import json
from .utils import query_api


# Create your views here.
def soloRecommendation(user=None, longitude=125.6018725, latitude=7.0689124, keyword=None):
	if keyword:
		# Search using keyword, longitude, latitude
		likes = query_api(longitude, latitude, keyword)['businesses']
		allRestaurants = query_api(longitude, latitude)['businesses']
		others = [x for x in allRestaurants if x not in likes]
		return HttpResponse(json.dumps({'related': likes, 'others': others}), content_type="application/json")
	else:
		# Preferences
		print("Hello")


def groupRecommendation(longitude, latitude, user, keyword=None):
	if keyword:
		# Searcch using keyword, longitude, latitude
		print("Hello")

	else:
		# Preferences
		print("Hello")
