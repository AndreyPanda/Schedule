from django.urls import  path

from main.views import choose_the_specialization, choose_the_doctor, choose_the_time, fill_in_the_client_data

urlpatterns = [
    path('', choose_the_specialization, name='specializations'),
    path('doctors/<slug:spec_slug>/', choose_the_doctor, name='doctors'),
    path('calendar/<slug:doct_slug>/', choose_the_time, name='calendar'),
    path('client_data/', fill_in_the_client_data, name='client_data'),
]