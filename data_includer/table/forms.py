from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *


class DatasetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Dataset
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'file': forms.FileInput(attrs={'accept': '.csv, .xlsx'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'form-textarea',
                                                 'placeholder': 'some simple description'}),
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))