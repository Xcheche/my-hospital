from base import models
from . import forms
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from doctor import models as doctor_models
from patient import models as patient_models

def register(request):
    # if request.user.is_authenticated:
    #     messages.info(request, "You are already logged in.")
    #     return redirect(reverse("home"))

    if request.method == "POST":
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            # Save the user to the database
            new_user = form.save()

            # Extract cleaned data
            full_name = form.cleaned_data["full_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            user_type = form.cleaned_data["user_type"]

            # Create related profile
            if user_type == "Doctor":
                doctor_models.Doctor.objects.create(user=new_user, full_name=full_name)
            else:
                patient_models.Patient.objects.create(user=new_user, full_name=full_name, email=email)

            # Authenticate and log in
            authenticated_user = authenticate(request, email=email, password=password)
            if authenticated_user:
                login(request, authenticated_user)
                messages.success(request, "Account created successfully.")
                return redirect(reverse("home"))

            messages.warning(request, "Account created, but automatic login failed. Please log in manually.")
    else:
        form = forms.UserRegisterForm()

    return render(request, "users/sign-up.html", {"form": form})

#login view


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("/")

    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Authenticate user (must have custom backend for email login)
            user_authenticate = authenticate(request, email=email, password=password)

            if user_authenticate is not None:
                login(request, user_authenticate)
                messages.success(request, "Logged in successfully.")

                next_url = request.GET.get("next", "/")
                return redirect(next_url)
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = forms.LoginForm()

    return render(request, "users/sign-in.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("login")
