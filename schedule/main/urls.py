from django.urls import  path

from main.views import choice_of_specialization, choice_of_doctor

urlpatterns = [
    path('', choice_of_specialization),
    path('doctors', choice_of_doctor),

]