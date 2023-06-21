import datetime
import urllib.parse
import pytest

from django.test import Client
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from main.models import Visit, Customer, Doctor


@pytest.mark.django_db
class TestVisitCreationLogic:
    params = {
        "doctor": "sidorov",
        "visit_datetime": "202306220800",
    }
    query_string = urllib.parse.urlencode(params)
    url = reverse("customer_data") + "?" + query_string
    form_data = {
        "last_name": "яяяя",
        "first_name": "яяяя",
        "fathers_name": "яяяя",
        "birth_date": "1992-05-05",
        "phone": "+9",
    }
    client = Client()

    def test_visit_create_positive(self, create_specs_and_doctors_and_customers):
        assert Visit.objects.count() == 0

        response = self.client.post(self.url, data=self.form_data, follow=True)
        assert response.status_code == 200
        assert Customer.objects.count() == 3
        assert Customer.objects.last().last_name == "яяяя"
        assert Visit.objects.count() == 1

    def test_visit_create_invalid_doctor_is_busy(
        self, create_specs_and_doctors_and_customers
    ):
        assert Visit.objects.count() == 0

        # Создаем визит в БД к определенному доктору на определенное время
        visit = Visit.objects.create(
            doctor_to_visit=Doctor.objects.get(slug="sidorov"),
            visit_datetime=datetime.datetime(2023, 6, 22, 8, 00),
            customer_visiting=Customer.objects.last(),
        )
        visit.save()

        # Обращаемся к странице "customer_data" с попыткой записать еще одного клиента на это же время
        response = self.client.post(self.url, data=self.form_data, follow=True)

        # Проверяем, что клиентов по-прежнему = 2 (из фикстуры), а визитов = 1 (созданный первым в этой функции)
        # Значит логика сработала верно и вторая запись на то же время не была создана
        assert Customer.objects.count() == 2
        assert Visit.objects.count() == 1

        # Также проверим, а куда же нас перенаправили
        # Получаем url, на который перенаправила нас страница с данными клиента
        assert response.status_code == 200
        redirect_chain = response.redirect_chain
        assert len(redirect_chain) > 0
        redirect_url, redirect_status = redirect_chain[-1]

        # Формируем ожидаемый url, на который должно нас перенаправить с учетом того, что время уже занято
        not_success_url = reverse_lazy("booking_is_failed")
        params = {
            "doctor": Doctor.objects.get(slug="sidorov").id,
            "visit_datetime": datetime.datetime(2023, 6, 22, 8, 00),
            "reason": "doctorisbusy",
        }
        expected_url = f"{not_success_url}?{urlencode(params)}"
        assert redirect_url == expected_url

    def test_visit_create_invalid_customer_already_booked_this_day(
        self, create_specs_and_doctors_and_customers
    ):
        # Создаем визит в БД к определенному доктору на определенный день
        Visit.objects.create(
            doctor_to_visit=Doctor.objects.get(slug="sidorov"),
            visit_datetime=datetime.datetime(2023, 6, 22, 8, 00),
            customer_visiting=Customer.objects.last(),
        )
        assert Visit.objects.count() == 1

        # Обращаемся к странице "customer_data" с попыткой записать того же клиента на тот же день на другое время
        params = {
            "doctor": "sidorov",
            "visit_datetime": "202306220900",
        }
        query_string = urllib.parse.urlencode(params)
        url = reverse("customer_data") + "?" + query_string
        form_data = {
            "last_name": "Майоров",
            "first_name": "Ульян",
            "fathers_name": "Олегович",
            "birth_date": "1985-05-05",
            "phone": "+7-906-456-2020",
        }
        response = self.client.post(url, data=form_data, follow=True)

        # Проверяем, что клиентов по-прежнему = 2 (из фикстуры), а визитов = 1 (созданный первым в этой функции)
        # Значит логика сработала верно и вторая запись на один день к тому же врачу не была создана
        assert Customer.objects.count() == 2
        assert Visit.objects.count() == 1

        # Также проверим, а куда же нас перенаправили
        # Получаем url, на который перенаправила нас страница с данными клиента
        assert response.status_code == 200
        redirect_chain = response.redirect_chain
        assert len(redirect_chain) > 0
        redirect_url, redirect_status = redirect_chain[-1]

        # Формируем ожидаемый url, на который должно нас перенаправить с учетом того, что на этот день
        # этого клиента не должны мы были записать дважды
        not_success_url = reverse_lazy("booking_is_failed")
        params = {
            "doctor": Doctor.objects.get(slug="sidorov").id,
            "visit_datetime": datetime.datetime(2023, 6, 22, 9, 00),
            "reason": "youalreadybookthisday",
        }
        expected_url = f"{not_success_url}?{urlencode(params)}"
        assert redirect_url == expected_url

        def test_visit_create_invalid_customer_is_busy_at_another_doctor(
            self, create_specs_and_doctors_and_customers
        ):
            # Создаем визит в БД к определенному доктору на определенный день
            Visit.objects.create(
                doctor_to_visit=Doctor.objects.get(slug="sidorov"),
                visit_datetime=datetime.datetime(2023, 6, 22, 8, 00),
                customer_visiting=Customer.objects.last(),
            )
            assert Visit.objects.count() == 1

            # Обращаемся к странице "customer_data" с попыткой записать того же клиента на то же время, но к
            # другому врачу
            params = {
                "doctor": "petrov",
                "visit_datetime": "202306220800",
            }
            query_string = urllib.parse.urlencode(params)
            url = reverse("customer_data") + "?" + query_string
            form_data = {
                "last_name": "Майоров",
                "first_name": "Ульян",
                "fathers_name": "Олегович",
                "birth_date": "1985-05-05",
                "phone": "+7-906-456-2020",
            }
            response = self.client.post(url, data=form_data, follow=True)

            # Проверяем, что клиентов по-прежнему = 2 (из фикстуры), а визитов = 1 (созданный первым в этой функции)
            # Значит логика сработала верно и вторая запись не была создана
            assert Customer.objects.count() == 2
            assert Visit.objects.count() == 1

            # Также проверим, а куда же нас перенаправили
            # Получаем url, на который перенаправила нас страница с данными клиента
            assert response.status_code == 200
            redirect_chain = response.redirect_chain
            assert len(redirect_chain) > 0
            redirect_url, redirect_status = redirect_chain[-1]

            # Формируем ожидаемый url, на который должно нас перенаправить с учетом того, что
            # клиент уже записан к другому врачу на это время
            not_success_url = reverse_lazy("booking_is_failed")
            params = {
                "doctor": Doctor.objects.get(slug="petrov").id,
                "visit_datetime": datetime.datetime(2023, 6, 22, 8, 00),
                "reason": "youhavevisittoanotherdoctor",
            }
            expected_url = f"{not_success_url}?{urlencode(params)}"
            assert redirect_url == expected_url
