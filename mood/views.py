from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from calendar import HTMLCalendar

from django.http import Http404
from django.shortcuts import render, redirect

from datetime import date

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

		try:
			d = Day.objects.filter(user__id=self.request.user.id).latest('date')
			e = Entry.objects.filter(day__id=d.id).order_by('-created')
			context['latest_entryset'] = e
			context['latest_day'] = d
			context['latest_date'] = d.date
			context['latest_day_value'] = d.date.day
			return context
		except:
			return context

	def get_user_id(self):
		return self.request.user.id;

	def get_username(self):
		return self.request.user.get_username()

	def get_name(self):
		u = self.request.user
		return u.get_full_name()

	def get_year(self):
		d = date.today()
		print(type(d))
		return d.year

	def get_month(self):
		d = date.today()
		return d.month



class DayCalendarView(LoginRequiredMixin, TemplateView):

	template_name = "mood/calendar.html"
 
	def show_calendar(self):
		year = self.kwargs.get('year')
		month = self.kwargs.get('month')
		month_int = int(month)
		year_int = int(year)
		dayset = Day.objects.filter(user__id=self.request.user.id).order_by('-date')
		cal = DayCalendar(dayset, self).formatmonth(year_int, month_int)
		return mark_safe(cal)

	def get_current_month(self):
		return date.today().month


class DayView(LoginRequiredMixin, TemplateView):

	model = Day

	template_name = "mood/day.html"
	context_object_name = "day"

	def dispatch(self, request, *args, **kwargs):
		day = Day.objects.get(pk=kwargs.get('pk'))
		if day.user_id == request.user.id:
			return super(DayView, self).dispatch(request, *args, **kwargs)
		else:
			raise Http404("Not Found")



	def get_context_data(self, **kwargs):
		context = super(DayView, self).get_context_data(**kwargs)

		dayset = Day.objects.filter(user__id=self.request.user.id)
		d = dayset.get(id=kwargs.get('pk'))
		e = Entry.objects.filter(day__id=d.id).order_by('-created')
		context['latest_entryset'] = e
		context['latest_day'] = d
		context['latest_date'] = d.date
		context['latest_day_value'] = d.date.day
		return context

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


class DayCreate(LoginRequiredMixin, TemplateView):

	model = Day
	context_object_name = "add_day"
	template_name = "mood/day.html"

	def dispatch(self, request, *args, **kwargs):
		u = User.objects.get(pk=self.kwargs.get('pk'))
		if u.id == request.user.id:
			selected_date = date(int(kwargs.get('year')), int(kwargs.get('month')), int(kwargs.get('day')))
			new_day = Day(date=selected_date, user=request.user)
			new_day.save()
			url = "/day/%s" % new_day.pk
			return redirect(url)
		else:
			raise Http404("Not Found")
		


class EntryCreate(LoginRequiredMixin, CreateView):

    model = Entry
    form_class = EntryAddForm

    def dispatch(self, request, *args, **kwargs):
    	d = Day.objects.get(pk=self.kwargs.get('pk'))
    	if d.user_id == request.user.id:
    		return super(EntryCreate, self).dispatch(request, *args, **kwargs)
    	else:
    		raise Http404("Not Found")

    def get_initial(self):
    	initial = super(EntryCreate, self).get_initial()

    	try:
    		e = Entry.objects.filter(user__id=self.request.user.id).latest('created')
    		initial['happiness_level'] = e.happiness_level
    		initial['motivation_level']  = e.motivation_level
    		initial['anger_level'] = e.anger_level
    		initial['anxiety_level'] = e.anxiety_level
    		initial['energy_level'] = e.energy_level
    		return initial
    	except:
    		initial['happiness_level']=0
    		initial['motivation_level']=0
    		initial['anger_level']=0
    		initial['anxiety_level']=0
    		initial['energy_level']=0
    		return initial



    def get_success_url(self):
    	return "/day/%s" % self.kwargs.get('pk')

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

	def dispatch(self, request, *args, **kwargs):
		e = Entry.objects.get(pk=self.kwargs.get('pk'))
		if e.user_id == request.user.id:
			return super(EntryDelete, self).dispatch(request, *args, **kwargs)
		else:
			raise Http404("Not Found")


class EntryUpdate(LoginRequiredMixin, UpdateView):

	model = Entry
	form_class = EntryUpdateForm
	template_name = "mood/entry_update.html"

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

	def get_success_url(self):
		entry = Entry.objects.get(pk=self.kwargs.get('pk'))
		d = Day.objects.get(pk=entry.day.id)
		return "/day/%s" % d.id

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
