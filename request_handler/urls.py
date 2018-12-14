from django.urls import path

from . import views

urlpatterns = [
    path('status', views.get_status, name='status'),
    path('report', views.report_status, name='report'),
    path('status2', views.get_status2, name='status2'),
    path('report2', views.report_status2, name='report2'),

    path('control', views.control, name='control'),
    path('get_control', views.get_control, name='get_control'),
]
