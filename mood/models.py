from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from mood.choices import *

class Profile(models.Model):
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
        )
	description = models.TextField('Add a Description')

	def __str__(self):
		return str(self.user.get_username())

class Day(models.Model):
	date = models.DateField()
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.date)

class Entry(models.Model):

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
        )

	tod = models.CharField(max_length=1, choices=TIME_OF_DAY_CHOICES)

	day = models.ForeignKey(Day, on_delete=models.CASCADE)
	happiness = models.IntegerField(choices=MOOD_RATING_CHOICES, default=0)
	sadness = models.IntegerField(choices=MOOD_RATING_CHOICES, default=0)
	anger = models.IntegerField(choices=MOOD_RATING_CHOICES, default=0)
	fear = models.IntegerField(choices=MOOD_RATING_CHOICES, default=0)

	energy_level = models.IntegerField(choices=MOOD_RATING_CHOICES, default=0)

	
	def __str__(self):
		return str(self.get_tod_display())

	def get_absolute_url(self):
		return reverse('entry', kwargs={'pk' : self.pk })


