from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from ceat.settings import DEFAULT_PREFS


class User(AbstractUser):
	"""
	Extends User Model, adding bio, birthdate, and groups 
	a user belongs to.
	"""
	username = models.CharField(_('username'), max_length=16, unique=True,
	    help_text=_('Required. 8-16 characters. Letters, digits and '
	                '@/./+/-/_ only.'),
	    validators=[
	        validators.RegexValidator(r'^[\w.@+-]+$',
	                                  _('Enter a valid username. '
	                                    'This value may contain only letters, numbers '
	                                    'and @/./+/-/_ characters.'), 'invalid'),
	        validators.MinLengthValidator(8, _('Username must be at least 8 characters')),
	    ],
	    error_messages={
	        'unique': _("A user with that username already exists."),
    })
	bio = models.TextField(max_length=500, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	preferences = models.TextField(blank=False, default=DEFAULT_PREFS)
	avatar_url = models.CharField(max_length=256, blank=True, null=True)

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


class History(models.Model):
	"""
	History model to log user experiences
	"""
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	resto = models.CharField(max_length=100)
	categories = models.CharField(max_length=100)
	isLiked = models.BooleanField()
	date_went = models.DateField(auto_now=True)


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
