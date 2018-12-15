from django.urls import path

from . import views

urlpatterns = [
    path('reporter', views.reporter, name='reporter'),
    path('', views.dashboard, name='dashboard'),
]
