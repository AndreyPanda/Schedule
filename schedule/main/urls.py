from django.urls import  path

from main.views import choice_of_specialization, choice_of_doctor, choice_of_time

urlpatterns = [
    path('', choice_of_specialization),
    path('doctors/<slug:spec_slug>/', choice_of_doctor, name='doctors'),
    path('calendar/<slug:doct_slug>/', choice_of_time, name='calendar'),
]