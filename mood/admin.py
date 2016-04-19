from django.contrib import admin

# Register your models here.
	
from .models import Day, Entry, News, Attribute, Consumable, Dietary, Drink

admin.site.register(Day)
admin.site.register(Entry)
admin.site.register(News)
admin.site.register(Attribute)
admin.site.register(Consumable)
admin.site.register(Dietary)
admin.site.register(Drink)
