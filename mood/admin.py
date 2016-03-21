from django.contrib import admin

# Register your models here.
	
from .models import Profile, Day

admin.site.register(Profile)
admin.site.register(Day)
