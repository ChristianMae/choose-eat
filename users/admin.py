from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Group, Friendship, History

# Register your models here.
admin.site.register(User)
admin.site.register(Friendship)
admin.site.register(Group)
admin.site.register(History)
