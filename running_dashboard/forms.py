import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from running_dashboard.models import Run
from running_dashboard.util import attributesFromGpx


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
    """
    Form that is intended to allow the user to add a new run to the db using an input field for a gpx file.
    The form is used by the `AddNewRun` view.
    """

    gpx_file = forms.FileField(label="Upload GPX file")


    def clean_gpx_file(self):
        
        data = self.cleaned_data['gpx_file']

        try:
            data = data.read().decode('utf-8')
            attributes = attributesFromGpx(data)

        except (UnicodeDecodeError, ValueError) as e:
            raise forms.ValidationError(
                "The file representing the run must be a gpx file with a recorded track")

        return attributes


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


