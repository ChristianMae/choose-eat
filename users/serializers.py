from rest_framework import serializers
from .models import User, History
import json

class UserDetailsSerializer(serializers.ModelSerializer):
    user_history = serializers.SerializerMethodField()

    def get_user_history(self, obj):
        try:
            myUser = User.objects.get(id=obj.id)
            userHistory = History.objects.filter(user=myUser)
            historyToReturn = []
            for history in userHistory:
                if history.isLiked in (True, False):
                    continue
                newHistory = dict()
                newHistory['id'] = history.id
                newHistory['resto'] = history.resto
                newHistory['categories'] = history.categories
                newHistory['isLiked'] = history.isLiked
                newHistory['date_went'] = str(history.date_went)
                historyToReturn.append(newHistory)
            return json.dumps(historyToReturn)
        except Exception as e:
            return str(e)

    user_ratedhistory = serializers.SerializerMethodField()

    def get_user_ratedhistory(self, obj):
        try:
            myUser = User.objects.get(id=obj.id)
            userHistory = History.objects.filter(user=myUser)
            historyToReturn = []
            for history in userHistory:
                if history.isLiked not in (True, False):
                    continue
                newHistory = dict()
                newHistory['id'] = history.id
                newHistory['resto'] = history.resto
                newHistory['categories'] = history.categories
                newHistory['isLiked'] = history.isLiked
                newHistory['date_went'] = str(history.date_went)
                historyToReturn.append(newHistory)
            return json.dumps(historyToReturn)
        except Exception as e:
            return str(e)


    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'bio', 'birth_date', 'preferences', 'avatar_url', 'date_joined', 'user_history', 'user_ratedhistory')
