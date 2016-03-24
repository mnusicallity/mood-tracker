from django.conf.urls import url, include
from django.views.generic import RedirectView

from mood.views import ProfileView, EntryListView, EntryCreate, EntryUpdate, EntryDelete

urlpatterns = [
	url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/$', ProfileView.as_view(), name='profile'),
    url(r'^$',  RedirectView.as_view(pattern_name="profile"), name="index"),
    url(r'^day/(?P<pk>[0-9]+)/$', EntryListView.as_view(), name='entry_list'),
    url(r'^entry/(?P<pk>[0-9]+)/$', EntryUpdate.as_view(), name='entry_edit'),
    url(r'^entry/delete/(?P<pk>[0-9]+)/$', EntryDelete.as_view(), name='entry_delete'),
    url(r'^entry/add/(?P<pk>[0-9]+)/$', EntryCreate.as_view(), name='entry_add'),
]