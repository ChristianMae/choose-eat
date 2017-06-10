from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserGroup(models.Model):
	"""
	Group model for group recommendations
	A user can create groups, name it, and add other users to it.
	"""
	name = models.CharField(max_length=50, blank=True, default='Unnamed Group')
	creator = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.name


class Profile(models.Model):
	"""
	Extends User Model, adding bio, birthdate, and groups 
	a user belongs to.
	"""
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	groups = models.ManyToManyField(UserGroup)


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
	Status = 0 (Pending request) | 1 (Accepted)
	"""
	user_a = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userA')
	user_b = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userB')
	friends = models.BooleanField(default=False)
