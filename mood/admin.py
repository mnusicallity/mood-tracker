from django.contrib import admin

# Register your models here.
	
from .models import Profile, Day, Entry

admin.site.register(Profile)
admin.site.register(Day)
admin.site.register(Entry)
