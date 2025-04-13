from django import forms
from django.contrib.auth.models import User


class Inscription(forms.ModelForm):
    password = forms.CharField(label='password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=('username','first_name','last_name','email')
        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] !=cd['password2']:
                raise forms.ValidationError('password does not match')
            return cd['password2']