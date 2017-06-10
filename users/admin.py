from django.contrib import admin
from .models import UserGroup, Profile, Friendship

# Register your models here.
admin.site.register(UserGroup)
admin.site.register(Profile)
admin.site.register(Friendship)