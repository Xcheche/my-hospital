from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("<int:year>/<int:month>/<int:day>/<slug:service_slug>/", views.service_detail, name="service_detail"),
    path("book/<int:service_id>/<int:doctor_id>/", views.book_appointment, name="book_appointment"),
    path("checkout/<str:billing_id>/", views.checkout, name="checkout"),

]
