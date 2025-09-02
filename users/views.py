from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegisterForm
from doctor import models as doctor_models
from patient import models as patient_models

def register(request):
    if request.user.is_authenticated:
        
        messages.success(request, "You are already logged in")
        return redirect("/")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            full_name = form.cleaned_data.get("full_name")
            email = form.cleaned_data.get("email")
            password1 = form.cleaned_data.get("password1")
            user_type = form.cleaned_data.get("user_type")

            # Create related profile
            if user_type == "Doctor":
                doctor_models.Doctor.objects.create(user=user, full_name=full_name)
            else:
                patient_models.Patient.objects.create(user=user, full_name=full_name, email=email)

            # Authenticate and login user
            authenticated_user = authenticate(request, email=email, password=password1)
            if authenticated_user:
                login(request, authenticated_user)
                messages.success(request, f"Account created successfully for {user_type.lower()} {full_name}")
                return redirect("/")

            messages.error(request, "Account created, but login failed. Please login manually.")
            return redirect("/login")
        else:
            # Show form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegisterForm()

    context = {"form": form}
    return render(request, "users/sign-up.html", context)

#login view


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("/")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Authenticate user (must have custom backend for email login)
            user_authenticate = authenticate(request, email=email, password=password)

            if user_authenticate is not None:
                login(request, user_authenticate)

                messages.success(request, "Logged in successfully. Welcome back!")

                next_url = request.GET.get("next", "/")
                return redirect(next_url)
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()

    return render(request, "users/sign-in.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("login")
