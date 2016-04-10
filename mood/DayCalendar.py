from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc

class DayCalendar(HTMLCalendar):

	def __init__(self, dayset, data):
		super(DayCalendar, self).__init__()
		print(data.kwargs)
		self.dayset = self.group_by_day(dayset)
		self.kwargs = data.kwargs
		self.data = data

	def formatday(self, day, weekday):
		if day != 0:
			cssclass = self.cssclasses[weekday]
			if date.today() >= date(self.year, self.month, day):
				cssclass += ' day_%i' % day
				if day in self.dayset:
					body = []
					for day_entry in self.dayset[day]:
						body.append('<p>')
						body.append('<a href="%s" class="stat_link">' % day_entry.get_absolute_url())
						body.append('View Stats</a>')
						body.append('</p>')
					return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
				body = []
				body.append('<p>')
				body.append('<a href="%s" class="add_link">' % ('/%s/%s/%i/add/%s' % (self.kwargs.get('year'), self.kwargs.get('month'), day, self.data.request.user.id)))
				body.append('Click to add</a>')
				body.append('</p>')
				return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
			return self.day_cell(cssclass, day)
		return self.day_cell('noday', '&nbsp;')

	def formatmonth(self, year, month, withyear=True):
		self.year = year
		self.month = month
		v = ['<table class="table month table-bordered">']
		v.append(self.formatmonthname(year, month, withyear=withyear))
		v.append(self.formatweekheader())
		for week in self.monthdays2calendar(year, month):
			v.append(self.formatweek(week))
		v.append('</table>')
		return ''.join(v)

	def group_by_day(self, dayset):
		field = lambda day_field: day_field.date.day
		return dict( [(day, list(items)) for day, items in groupby(dayset, field)])

	def day_cell(self, cssclass, body):
		return '<td class="%s">%s</td>' % (cssclass, body)
