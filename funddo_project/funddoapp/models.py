from django.db import models
from django.contrib.auth.models import User, AbstractUser
from funddoapp.location import LOCATION_CHOICES
from django.utils.timezone import now
# Create your models here.



class UserProfile(models.Model):
	user = models.OneToOneField(User)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	bio = models.TextField()
	services = models.TextField(blank=True)
	funder = models.BooleanField(default=False, blank=True)
	jobseeker = models.BooleanField(default=False, blank=True)
	your_location = models.IntegerField(choices=LOCATION_CHOICES, default=1)

	def __unicode__(self):
		return self.user.username


class Request(models.Model):
	poster = models.ForeignKey(User)
	title = models.CharField(max_length=128)
	request = models.TextField()
	email = models.EmailField(max_length=255)
	posted_on = models.DateTimeField(default=now)
	

	def __unicode__(self):
		return self.title