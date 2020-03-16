import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from running_dashboard.models import Run


class ChangeRunDurationForm(forms.Form):

    # id = forms.AutoField(primary_key=True)
    # time_sec = forms.PositiveIntegerField()
    time_sec = forms.IntegerField()
    # route = forms.LineStringField()
    # runner = forms.ForeignKey()

    def clean_time_sec(self):
        data = self.cleaned_data['time_sec']

        if data < 0:
            raise ValidationError('The duration can\'t be a negative number')

        return data


class AddRunForm(forms.Form):

    start_time = forms.DateTimeField(label="Start Time", widget=forms.DateTimeInput(attrs= {'placeholder':"2019-12-31 16:30:00"}))
    time_sec = forms.IntegerField(label="Duration")
    # route = forms.FileField(label="Route (Upload GPX file)")

    def clean(self):

        data = self.cleaned_data

        return data

    class Meta:
        model = Run
