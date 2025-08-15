from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),  # Uncomment if you have a login view
    path("logout/", views.logout_view, name="logout"),  # Uncomment if you have a logout view
]
