import calendar
import locale
from datetime import timedelta, datetime

from django.db.models import Q
from django.urls import reverse_lazy

from main.forms import AddClient
from main.models import Specialization, Doctor, Visit, Client
from django.views.generic import TemplateView, CreateView
from django.utils.http import urlencode

locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")


class ChooseTheSpecialization(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        specialists = Specialization.objects.filter(
            is_used=True, doctors_specialization__isnull=False
        ).distinct()
        button_count = len(specialists)
        buttons_per_row = 3
        rows = []
        spec_titles = iter(specialists)

        for i in range(button_count // buttons_per_row):
            row = []
            for j in range(buttons_per_row):
                row.append(next(spec_titles))
            rows.append(row)

        row = []
        for i in range(button_count % buttons_per_row):
            row.append(next(spec_titles))
        rows.append(row)

        context = {
            "rows": rows,
        }

        return context


class ChooseTheDoctor(TemplateView):
    template_name = "main/doctors.html"

    def get_context_data(self, **kwargs):
        doctors = Doctor.objects.filter(
            is_active=True, specialization__slug=self.request.GET.get("spec")
        )
        button_count = len(doctors)
        buttons_per_row = 3
        rows = []
        doctor_titles = iter(doctors)

        for i in range(button_count // buttons_per_row):
            row = []
            for j in range(buttons_per_row):
                row.append(next(doctor_titles))
            rows.append(row)

        row = []
        for i in range(button_count % buttons_per_row):
            row.append(next(doctor_titles))
        rows.append(row)

        context = {
            "rows": rows,
            "spec_slug": self.request.GET.get("spec"),
            "specialization": Specialization.objects.get(
                slug=self.request.GET.get("spec")
            ).title,
        }

        return context


class VisitDatetime:
    def __init__(self, start_time, finish_time, visit_date):
        self.start_time = start_time
        self.finish_time = finish_time
        self.visit_date = visit_date

    def get_visit_datetime(self):
        return datetime.combine(self.visit_date, self.start_time).strftime("%Y%m%d%H%M")

    def __str__(self):
        return f"{self.start_time.strftime('%H:%M')} - {self.finish_time.strftime('%H:%M')}"


class ChooseTheTime(TemplateView):
    template_name = "main/visits.html"

    def get_context_data(self, **kwargs):
        doctor = Doctor.objects.get(slug=self.request.GET.get("doctor_slug"))
        # Вводим здесь дату, так как к типу данных TimeField нельзя применить метод combine
        inner_needed_date = datetime(1900, 1, 1)
        start = datetime.combine(inner_needed_date, doctor.working_start_time)
        finish = datetime.combine(
            inner_needed_date, doctor.working_finish_time
        ) + timedelta(minutes=30)
        button_count = len(str(doctor.working_days)) * (finish - start).seconds // 1800
        button_per_row = len(str(doctor.working_days))
        rows = []
        start = doctor.working_start_time

        for i in range(button_count // button_per_row):
            row = []
            if i == 0:
                # Формируем данные для первой строки. Это надписи в формате "Понедельник 29 мая 2023"
                months = {
                    "Январь": "января",
                    "Февраль": "февраля",
                    "Март": "марта",
                    "Апрель": "апреля",
                    "Май": "мая",
                    "Июнь": "июня",
                    "Июль": "июля",
                    "Август": "августа",
                    "Сентябрь": "сентября",
                    "Октябрь": "октября",
                    "Ноябрь": "ноября",
                    "Декабрь": "декабря",
                }
                for day_index in range(len(str(doctor.working_days))):
                    # Получаем номер дня недели для сегодняшнего дня (0 - понедельник, 1 - вторник, и т.д.)
                    today_weekday = datetime.today().weekday()
                    # Получаем дату понедельника текущей недели
                    start_of_week = datetime.today() - timedelta(days=today_weekday)
                    # Получаем даты всех рабочих дней врача на текущей неделе
                    dates_of_week = [
                        start_of_week + timedelta(days=int(i) - 1)
                        for i in str(doctor.working_days)
                    ]
                    # Заменяем в полученной дате название месяца (например Май -> мая)
                    for k, v in months.items():
                        if k in dates_of_week[day_index].strftime("%d %B %Y"):
                            result_date = (
                                dates_of_week[day_index]
                                .strftime("%d %B %Y")
                                .replace(k, v)
                            )
                            break
                    # Добавляем в переменную row список с днем недели и датой
                    row.append(
                        [calendar.day_name[int(day_index)].capitalize(), result_date]
                    )
                rows.append(row)
            # Формируем данные для отображения на кнопках с интервалами времени
            else:
                today_weekday = datetime.today().weekday()
                start_of_week = datetime.today() - timedelta(days=today_weekday)
                dates_of_week = [
                    start_of_week + timedelta(days=int(i) - 1)
                    for i in str(doctor.working_days)
                ]
                for button in range(button_per_row):
                    doctor_lunch_center_in_date = datetime.combine(
                        datetime(1990, 1, 1), doctor.lunch_start_time
                    ) + timedelta(minutes=30)
                    doctor_lunch_center_in_time = doctor_lunch_center_in_date.time()
                    inner_needed_date = dates_of_week[button]
                    datetime_obj = datetime.combine(inner_needed_date, start)
                    if Visit.objects.filter(
                        Q(visit_datetime=datetime_obj) & Q(doctor_to_visit=doctor)
                    ).exists() or datetime_obj.time() in (
                        doctor.lunch_start_time,
                        doctor_lunch_center_in_time,
                    ):
                        row.append(
                            [
                                "Недоступно",
                            ]
                        )
                    else:
                        increased_datetime_obj = datetime_obj + timedelta(minutes=30)
                        increased_time = increased_datetime_obj.time()
                        row.append(
                            VisitDatetime(start, increased_time, dates_of_week[button])
                        )
                rows.append(row)

                inner_needed_date = datetime(1900, 1, 1)
                datetime_obj = datetime.combine(inner_needed_date, start)
                increased_datetime_obj = datetime_obj + timedelta(minutes=30)
                start = increased_datetime_obj.time()

        context = {
            "rows": rows,
            "doct_slug": self.request.GET.get("doctor_slug"),
        }

        return context


class FillInTheClientData(CreateView):
    form_class = AddClient
    template_name = "main/client_data.html"

    def form_valid(self, form):
        visit_string = self.request.GET.get("visit_datetime")
        visit_datetime = datetime(
            int(visit_string[:4]),
            int(visit_string[4:6]),
            int(visit_string[6:8]),
            int(visit_string[8:10]),
            int(visit_string[10:]),
        )
        doctor_id = Doctor.objects.get(slug=self.request.GET.get("doctor")).id

        if form.is_valid():
            if not Visit.objects.filter(
                Q(visit_datetime=visit_datetime)
                & Q(doctor_to_visit=Doctor.objects.get(pk=doctor_id))
            ):
                new_client = form.save()
                new_visit = Visit(
                    visit_datetime=visit_datetime,
                    doctor_to_visit=Doctor.objects.get(pk=doctor_id),
                    client_visiting=Client.objects.get(pk=new_client.id),
                )
                new_visit.save()
                success_url = reverse_lazy("booking_is_created")
                params = {"doctor": doctor_id, "visit_datetime": visit_datetime}
                url = f"{success_url}?{urlencode(params)}"
                self.success_url = url
            else:
                not_success_url = reverse_lazy("booking_is_failed")
                params = {"doctor": doctor_id, "visit_datetime": visit_datetime}
                url = f"{not_success_url}?{urlencode(params)}"
                self.success_url = url

        return super().form_valid(form)


class BookingIsCreated(TemplateView):
    template_name = "main/booking_is_created.html"

    def get_context_data(self, **kwargs):
        context = {
            "doctor": Doctor.objects.get(pk=self.request.GET.get("doctor")),
            "visit_datetime": self.request.GET.get("visit_datetime"),
        }
        return context


class BookingIsFailed(TemplateView):
    template_name = "main/booking_is_failed.html"

    def get_context_data(self, **kwargs):
        context = {
            "doctor": Doctor.objects.get(pk=self.request.GET.get("doctor")),
            "visit_datetime": self.request.GET.get("visit_datetime"),
        }
        return context
