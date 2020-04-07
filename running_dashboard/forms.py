import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
    route = forms.FileField(label="Route (Upload GPX file)")

    def clean(self):

        data = self.cleaned_data

        return data

    class Meta:
        model = Run


class UniqueUserEmailField(forms.EmailField):
    """
    An EmailField which only is valid if no User has that email.
    """
    def validate(self, value):
        super(forms.EmailField, self).validate(value)
        try:
            User.objects.get(email=value)
            raise forms.ValidationError("A user with that email is already registered")
        except User.MultipleObjectsReturned:
            raise forms.ValidationError("A user with that email is already registered")
        except User.DoesNotExist:
            pass


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, help_text="")
    email = UniqueUserEmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


