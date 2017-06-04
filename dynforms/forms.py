from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, MaxLengthValidator
from django.utils.translation import ugettext as _


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


class RegistrationForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    email = forms.EmailField(required=True, validators=[EmailValidator()])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise ValidationError(_('Nazwa użytkownika jest już zajęta'))
        return self.cleaned_data['username']


class NewLanguageForm(forms.Form):
    code = forms.CharField(required=True, validators=[MaxLengthValidator(20)])
    name = forms.CharField(required=True, validators=[MaxLengthValidator(100)])


class NewFormTemplateForm(forms.Form):
    name = forms.CharField(label=_('Nazwa'), required=True, validators=[MaxLengthValidator(100)],
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label=_('Opis'), widget=forms.Textarea(attrs={'class': 'form-control'}),
                                  required=True, validators=[MaxLengthValidator(1000)])
    max_submissions = forms.IntegerField(label=_('Maksymalna liczba zgłoszeń'), initial=0,
                                         widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                         required=False)
