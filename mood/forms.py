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

	tod = forms.ChoiceField(choices = TIME_OF_DAY_CHOICES, label="Time of Day", required=True)

	happiness = forms.IntegerField(label="Happiness Level:", widget=forms.TextInput(attrs={'class':'entry_field'}))
	sadness = forms.IntegerField(label="Sadness Level:", widget=forms.TextInput(attrs={'class':'entry_field'}))
	anger = forms.IntegerField(label="Anger/Disgust Level:", widget=forms.TextInput(attrs={'class':'entry_field'}))
	fear = forms.IntegerField(label="Fear/Surpise Level:", widget=forms.TextInput(attrs={'class':'entry_field'}))
	energy_level = forms.IntegerField(label="Energy Level:", widget=forms.TextInput(attrs={'class':'entry_field'}))
