from django.shortcuts import render
from django.views.generic.base import TemplateView

from mood.models import Profile
from django.contrib.auth.models import User
# Create your views here.

class ProfileView(TemplateView):

	template_name = "mood/profile.html"
	context_object_name = "user_profile"
	

	def get_username(self):
		return self.request.user.get_username()
		
	def get_desc(self):
		u = self.request.user
		p = Profile.objects.filter(user__id=u.id)
		return p[0].description