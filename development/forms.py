"""
Made By: Shubham Heda
Developed Projects :: Django, Celery, Python, Rails and Angular
Under:  AppWallaz Company
"""

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from development.models import Contact

User._meta.get_field('email')._unique = True


# User._meta.get_field('username').__dict__['max_length'] = 75
# from .models import ConfirmationUser


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=100, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


# class ConfirmationForm(forms.ModelForm):
#     first_name = forms.CharField(max_length=30, required=True, help_text="Required Field")
#     last_name = forms.CharField(max_length=30, required=True, help_text="Required")
#     email = forms.EmailField(max_length=254, help_text="Required. Inform a valid email address")
#
#     class Meta:
#         model = ConfirmationUser
#         fields = ('username', 'first_name', 'last_name', 'email', 'password')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, Invalid Email Address or Password..!!!")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class ForgetForm(forms.Form):
    email = forms.CharField(max_length=100, required=True)

    def clean(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).exists()
        if not user:
            raise forms.ValidationError("Sorry Email Field Does not exist!!!")
        return self.cleaned_data

    def check_user(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email)
        if not user.exists():
            raise forms.ValidationError("Sorry Email Field Does not exist!!!")
        return user[0]


class ResetForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, label='Confirm Password')

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 == password2:
            return self.cleaned_data
        else:
            raise forms.ValidationError("Confirmation of Password failed @!@@!@!@!@")

    def check_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 == password2:
            return password2
        else:
            raise forms.ValidationError("Confirmation of password failed @!@@!@!@!@")


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'name',
            'email',
            'subject',
            'text',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Name', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'Enter Email ID', 'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Enter Mobile No.', 'class': 'form-control'}),
            'text': forms.Textarea(attrs={'placeholder': 'Enter Message', 'class': 'form-control'}),
        }


class NotesForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput)
    status = forms.CharField(widget=forms.HiddenInput)
    text = forms.CharField(widget=forms.Textarea(), initial='')


class SearchForm(forms.Form):
    search_data = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
