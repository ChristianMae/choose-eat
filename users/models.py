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

	# Look into using external text file
	default_prefs = "{'Afghan': 0, 'African': 0, 'Arabian': 0, 'Argentine': 0, 'Asian Fusion': 0, 'Australian': 0, 'Austrian': 0, 'Bangladeshi': 0, 'Basque': 0, 'Barbeque': 0, 'Belgian': 0, 'Bistros': 0, 'Brasseries': 0, 'Brazilian': 0, 'Breakfast & Brunch': 0, 'British': 0, 'Buffets': 0, 'Bulgarian': 0, 'Burgers': 0, 'Burmese': 0, 'Cafes': 0, 'Cafeteria': 0, 'Cajun/Creole': 0, 'Cambodian': 0, 'Caribbean': 0, 'Chicken Shop': 0, 'Chinese': 0, 'Creperies': 0, 'Cuban': 0, 'Delis': 0, 'Diners': 0, 'Dinner Theater': 0, 'Ethiopian': 0, 'Filipino': 0, 'Fish & Chips': 0, 'Fondue': 0, 'Food Court': 0, 'Food Stands': 0, 'French': 0, 'Gastropubs': 0, 'German': 0, 'Gluten-Free': 0, 'Greek': 0, 'Guamanian': 0, 'Halal': 0, 'Hawaiian': 0, 'Himalayan/Nepalese': 0, 'Honduran': 0, 'Hot Dogs': 0, 'Fast Food': 0, 'Hot Pot': 0, 'Hungarian': 0, 'Indonesian': 0, 'Indian': 0, 'Irish': 0, 'Italian': 0, 'Japanese': 0, 'Kebab': 0, 'Korean': 0, 'Kosher': 0, 'Laotian': 0, 'Latin American': 0, 'Malaysian': 0, 'Mediterranean': 0, 'Mexican': 0, 'Middle Eastern': 0, 'Modern European': 0, 'Mongolian': 0, 'Moroccan': 0, 'Nicaraguan': 0, 'Noodles': 0, 'Pakistani': 0, 'Pan Asian': 0, 'Persian/Iranian': 0, 'Peruvian': 0, 'Pizza': 0, 'Polish': 0, 'Pop-Up Restaurants': 0, 'Portuguese': 0, 'Live/Raw Food': 0, 'Russian': 0, 'Salad': 0, 'Sandwiches': 0, 'Scandinavian': 0, 'Seafood': 0, 'Singaporean': 0, 'Soup': 0, 'Spanish': 0, 'Sri Lankan': 0, 'Steakhouses': 0, 'Sushi Bars': 0, 'Syrian': 0, 'Taiwanese': 0, 'Tapas Bars': 0, 'Tapas/Small Plates': 0, 'Tex-Mex': 0, 'Thai': 0, 'American (Traditional)': 0, 'Turkish': 0, 'Ukrainian': 0, 'Vegan': 0, 'Vegetarian': 0, 'Vietnamese': 0, 'Waffles': 0, 'Wok': 0}"
	preferences = models.TextField(default=default_prefs)

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
