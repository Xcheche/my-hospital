from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Full Name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "*************"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "*************"}))
    user_type = forms.CharField(widget=forms.Select(choices=[("Doctor", "Doctor"), ("Patient", "Patient")]))


    class Meta:
        model = User
        fields = ("full_name", "email", "user_type", "password1", "password2")





class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "*************"}))



    class Meta:
        model = User
        fields = ("email", "password")

