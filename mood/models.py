from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from mood.choices import *

class Day(models.Model):
	date = models.DateField()
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
        )
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.created) + " date: " + str(self.date)

	def get_absolute_url(self):
		return reverse('day', kwargs={'pk' : self.pk })

	def get_add_url(self):
		return reverse('day_add', kwargs={'user_id' : self.user.id })

class Entry(models.Model):
	description = models.CharField(max_length=1000, null=True, blank=True)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
        )

	tod = models.CharField(max_length=1, choices=TIME_OF_DAY_CHOICES)
	created = models.DateTimeField(auto_now_add=True)

	day = models.ForeignKey(Day, on_delete=models.CASCADE)

	happiness_level = models.IntegerField(choices=MOOD_RATING_CHOICES, default=0)
	anger_level = models.IntegerField(choices=MOOD_RATING_CHOICES, default=0)
	anxiety_level = models.IntegerField(choices=MOOD_RATING_CHOICES, default=0)
	energy_level = models.IntegerField(choices=MOOD_RATING_CHOICES, default=0)
	motivation_level = models.IntegerField(choices=MOOD_RATING_CHOICES, default=0)

	
	def __str__(self):
		return str(self.get_tod_display())

	def get_absolute_url(self):
		return reverse('entry_edit', kwargs={'pk' : self.pk })


class News(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	date = models.DateField()
	title = models.CharField(max_length=50)
	content = models.TextField()

	def __str__(self):
		return self.title





