from django.contrib import admin

# Register your models here.
	
from .models import Day, Entry

admin.site.register(Day)
admin.site.register(Entry)
