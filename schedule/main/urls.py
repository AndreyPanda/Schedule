from django.urls import  path

from main.views import choice_of_specialization

urlpatterns = [
    path('', choice_of_specialization),
]