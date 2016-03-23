from django.contrib.auth import get_user_model
from django import forms

from django.utils.translation import ugettext_lazy as _


from mood.models import Profile, Day, Entry

from mood.choices import *

class SignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name' , 'last_name']

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        p = Profile(user=user, description="")
        p.save()

class EntryAddForm(forms.ModelForm):
	class Meta:
		model = Entry
		exclude = ['day','user']

	name = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Add a Name for the Entry (Optional)'}))

	tod = forms.ChoiceField(choices = TIME_OF_DAY_CHOICES, label = "Time of Day", required=True, widget=forms.Select(attrs={'class':'entry_field'}))

	happiness_level = forms.IntegerField(widget=forms.TextInput(attrs={'class':'entry_field'}))
	motivation_level = forms.IntegerField(widget=forms.TextInput(attrs={'class':'entry_field'}))
	anger_level = forms.IntegerField(widget=forms.TextInput(attrs={'class':'entry_field'}))
	anxiety_level = forms.IntegerField(widget=forms.TextInput(attrs={'class':'entry_field'}))
	energy_level = forms.IntegerField(widget=forms.TextInput(attrs={'class':'entry_field'}))
