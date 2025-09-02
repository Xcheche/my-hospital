from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # Your custom user model
# Define USER_TYPE choices globally
USER_TYPE = [
    ("doctor", "Doctor"),
    ("patient", "Patient"),
]

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "John Doe"})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "johndoe@gmail.com"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "*************"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "*************"})
    )
    user_type = forms.ChoiceField(
        choices=USER_TYPE,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = User
        fields = ["full_name", "email", "password1", "password2", "user_type"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.user_type = self.cleaned_data["user_type"].lower()  # store lowercase if needed
        user.set_password(self.cleaned_data["password1"])  # Hash the password

        if commit:
            user.save()
        return user
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'johndoe@gmail.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*************'}))

    class Meta:
        model = User
        fields = ['email', 'password']