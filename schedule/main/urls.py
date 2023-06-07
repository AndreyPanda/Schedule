from django.urls import path
from django.contrib import admin

from main.views import (
    ChooseTheSpecialization,
    ChooseTheDoctor,
    ChooseTheTime,
    FillInTheClientData,
    BookingIsCreated,
    BookingIsFailed,
    Register,
    Login,
    logout_user,
)


urlpatterns = [
    path("admin/", admin.site.urls, name="admin:index"),
    path("", ChooseTheSpecialization.as_view(), name="specializations"),
    path("doctors/", ChooseTheDoctor.as_view(), name="doctors"),
    path("calendar/", ChooseTheTime.as_view(), name="calendar"),
    path("client_data/", FillInTheClientData.as_view(), name="client_data"),
    path("booking_ok/", BookingIsCreated.as_view(), name="booking_is_created"),
    path("booking_nok/", BookingIsFailed.as_view(), name="booking_is_failed"),
    path("register/", Register.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
]
