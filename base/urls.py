from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("<int:year>/<int:month>/<int:day>/<slug:service_slug>/", views.service_detail, name="service_detail")

]
