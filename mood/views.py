from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from calendar import HTMLCalendar

from django.http import Http404

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.dates import MonthArchiveView

from mood.models import Day, Entry

from mood.DayCalendar import DayCalendar

from django.utils.safestring import mark_safe

from django.contrib.auth.mixins import LoginRequiredMixin

from mood.forms import EntryAddForm, EntryUpdateForm
from django.contrib.auth.models import User

# Create your views here.

class ProfileView(LoginRequiredMixin, TemplateView):

	template_name = "mood/profile.html"
	context_object_name = "user_profile"

	def get_context_data(self, **kwargs):
		context = super(ProfileView, self).get_context_data(**kwargs)

		d = Day.objects.filter(user__id=self.request.user.id).latest('date')
		e = Entry.objects.filter(day__id=d.id).order_by('-created')
		context['latest_entryset'] = e
		context['latest_day'] = d
		context['latest_date'] = d.date
		context['latest_day_value'] = d.date.day
		return context

	def get_user_id(self):
		return self.request.user.id;

	def get_username(self):
		return self.request.user.get_username()

	def get_name(self):
		u = self.request.user
		return u.get_full_name()

class DayCalendarView(LoginRequiredMixin, TemplateView):

	template_name = "mood/calendar.html"
 
	def show_calendar(self):
		year = self.kwargs.get('year')
		month = self.kwargs.get('month')
		month_int = int(month)
		year_int = int(year)
		dayset = Day.objects.filter(user__id=self.request.user.id).order_by('-date')
		cal = DayCalendar(dayset, self.request.user.id).formatmonth(year_int, month_int)
		return mark_safe(cal)

class EntryListView(LoginRequiredMixin, ListView):

	model = Entry

	template_name = "mood/entry_list.html"
	context_object_name = "entry_list"

	def get_day_id(self):
		return self.kwargs.get('pk')

	def get_queryset(self):
		d_id = self.kwargs.get('pk')
		entryset = Entry.objects.filter(day__id=d_id)
		return entryset

	def get_date(self):
		d_id = self.kwargs.get('pk')
		p = Day.objects.get(pk=d_id)
		return p.date



class EntryCreate(LoginRequiredMixin, CreateView):

    model = Entry
    form_class = EntryAddForm
    success_url = "/accounts/profile"

    def get_initial(self):
    	initial = super(EntryCreate, self).get_initial()

    	initial['happiness_level']=0
    	initial['motivation_level']=0
    	initial['anger_level']=0
    	initial['anxiety_level']=0
    	initial['energy_level']=0
    	
    	e = Entry.objects.filter(user__id=self.request.user.id).latest('created')

    	if e:
	    	initial['happiness_level'] = e.happiness_level
	    	initial['motivation_level']  = e.motivation_level
	    	initial['anger_level'] = e.anger_level
	    	initial['anxiety_level'] = e.anxiety_level
	    	initial['energy_level'] = e.energy_level

    	return initial

    def get_date(self):
    	d = Day.objects.get(pk=self.kwargs.get('pk'))
    	return d.date

    def form_valid(self, form):
    	f = form.save(commit=False)
    	f.day = Day.objects.get(pk=self.kwargs.get('pk'))
    	f.user = self.request.user
    	return super(EntryCreate, self).form_valid(form)

class EntryDelete(LoginRequiredMixin, DeleteView):

	model = Entry
	success_url = "/accounts/profile"


class EntryUpdate(LoginRequiredMixin, UpdateView):

	model = Entry
	form_class = EntryUpdateForm
	template_name = "mood/entry_update.html"
	success_url = "/accounts/profile"

	def dispatch(self, request, *args, **kwargs):
		e = Entry.objects.get(pk=self.kwargs.get('pk'))
		if e.user_id == request.user.id:
			return super(EntryUpdate, self).dispatch(request, *args, **kwargs)
		else:
			raise Http404("Not Found")

	def get_initial(self):
		initial = super(EntryUpdate, self).get_initial()
		e = Entry.objects.get(pk=self.kwargs.get('pk'))
		initial['happiness_level'] = e.happiness_level
		initial['motivation_level']  = e.motivation_level
		initial['anger_level'] = e.anger_level
		initial['anxiety_level'] = e.anxiety_level
		initial['energy_level'] = e.energy_level
		return initial

	def get_date(self):
		d = Day.objects.get(entry__id=self.kwargs.get('pk'))
		return d.date

	def tod_display(self):
		e = Entry.objects.get(pk=self.kwargs.get('pk'))
		return e.get_tod_display()

	def tod_num(self):
		e = Entry.objects.get(pk=self.kwargs.get('pk'))
		tod = e.tod
		switch = {
			"M":0,
			"A":1,
			"E":2,
			"N":3,
		}
		return str(switch.get(tod))
