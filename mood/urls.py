from django.conf.urls import url, include

from mood.views import ProfileView

urlpatterns = [
	url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/$', ProfileView.as_view()),
]