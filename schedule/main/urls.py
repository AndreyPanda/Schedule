from django.urls import  path

from main.views import choice_of_specialization, choice_of_doctor, choice_of_time

urlpatterns = [
    path('', choice_of_specialization),
    path('doctors/<int:spec_id>/', choice_of_doctor, name='doctors'),
    path('calendar/<int:doct_id>/', choice_of_time, name='calendar'),
]