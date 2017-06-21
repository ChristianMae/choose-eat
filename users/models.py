from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from ceat.settings import DEFAULT_PREFS


class UserGroup(models.Model):
	"""
	Group model for group recommendations
	A user can create groups, name it, and add other users to it.
	"""
	name = models.CharField(max_length=50, blank=True, default='Unnamed Group')
	creator = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return '{} (by {})'.format(self.name, self.creator)


class Profile(models.Model):
	"""
	Extends User Model, adding bio, birthdate, and groups 
	a user belongs to.
	"""
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	groups = models.ManyToManyField(UserGroup, blank=True)
	preferences = models.TextField(default=DEFAULT_PREFS)

	def __str__(self):
		return "{}'s profile".format(self.user.username)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Friendship(models.Model):
	"""
	Relationship of UserA and UserB (for Friend List)
	Friends = 0 (Pending request) | 1 (Accepted)
	"""
	user_a = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userA')
	user_b = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userB')
	friends = models.BooleanField(default=False)

	def __str__(self):
		return '{} -> {} ({})'.format(self.user_a.username, self.user_b.username, 'Friends' if self.friends else 'Pending')
