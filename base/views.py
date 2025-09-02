from django.shortcuts import get_object_or_404, render
from base import models as base_models
# Create your views here.

def home(request):
    services = base_models.Service.published.filter(status='PB').order_by('-publish')[:6]
    context = {'services': services}
    return render(request, "base/index.html", context)

from datetime import date

def service_detail(request, year, month, day, service_slug):
    target_date = date(int(year), int(month), int(day))
    service = get_object_or_404(
        base_models.Service.published,
        slug=service_slug,
        publish__date=target_date
    )
    context = {'service': service}
    return render(request, "base/service_detail.html", context)