from django.conf.urls import url, include
from django.views.generic import RedirectView

from mood.views import ProfileView, DayView, EntryCreate, EntryUpdate, EntryDelete, DayCalendarView, DayCreate

urlpatterns = [
	url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/$', ProfileView.as_view(), name='profile'),
    url(r'^$',  RedirectView.as_view(pattern_name="profile"), name="index"),
    url(r'^day/(?P<pk>[0-9]+)/$', DayView.as_view(), name='day'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/add/(?P<pk>[0-9]+)/$', DayCreate.as_view(), name='day_add'),
    url(r'^entry/(?P<pk>[0-9]+)/$', EntryUpdate.as_view(), name='entry_edit'),
    url(r'^entry/delete/(?P<pk>[0-9]+)/$', EntryDelete.as_view(), name='entry_delete'),
    url(r'^entry/add/(?P<pk>[0-9]+)/$', EntryCreate.as_view(), name='entry_add'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', DayCalendarView.as_view(), name="day_month"),
]