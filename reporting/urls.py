from django.urls import path
from .views import verbose_report

urlpatterns = [
    path('', verbose_report, name='verbose_report'),
]