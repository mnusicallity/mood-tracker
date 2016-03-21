from django.db import models
from django.conf import settings

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


