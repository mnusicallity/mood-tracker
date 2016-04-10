from django.contrib import admin

# Register your models here.
	
from .models import Day, Entry, News

admin.site.register(Day)
admin.site.register(Entry)
admin.site.register(News)
