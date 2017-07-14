from django.db import models
from django.contrib.auth.models import AbstractUser
from ceat.settings import DEFAULT_PREFS


class User(AbstractUser):
	"""
	Extends User Model, adding bio, birthdate, and groups 
	a user belongs to.
	"""
	bio = models.TextField(max_length=500, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	preferences = models.TextField(blank=False, default=DEFAULT_PREFS)

	def __str__(self):
		return "{}".format(self.username)

	def __int__(self):
		return int(self.pk)


class Group(models.Model):
	"""
	Group model for group recommendations
	A user can create groups, name it, and add other users to it.
	"""
	name = models.CharField(max_length=80, blank=True, default='Unnamed Group')
	creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
	members = models.ManyToManyField(User, blank=True, related_name='members')

	def __str__(self):
		return '{} (by {})'.format(self.name, self.creator)


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
