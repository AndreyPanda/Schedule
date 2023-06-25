from django.urls import reverse
from main.views import ChooseTheSpecialization


def test_choose_the_specialization(create_specs_and_doctors_and_customers, client):
    url = reverse("specializations")
    response = client.get(url)
    assert response.status_code == 200
    assert "Специализация 1" in response.content.decode("utf-8")
    assert "Специализация 2" in response.content.decode("utf-8")

    context = ChooseTheSpecialization().get_context_data()
    assert (
        len(context["rows"]) == 1
    )  # Проверка, что есть только одна строка со специализациями
    assert (
        len(context["rows"][0]) == 2
    )  # Проверка, что в тестовой БД есть только две специализации


def test_choose_the_doctor(create_specs_and_doctors_and_customers, client):
    url = reverse("doctors") + "?spec=spec1"
    response = client.get(url)
    assert response.status_code == 200
    assert "Сидоров" in response.content.decode("utf-8")


def test_choose_the_time(create_specs_and_doctors_and_customers, client):
    url = reverse("calendar") + "?doctor_slug=sidorov"
    response = client.get(url)
    assert response.status_code == 200


def test_fill_in_the_customer_data(create_specs_and_doctors_and_customers, client):
    url = reverse("customer_data") + "?visit_datetime=202306150800" + "?doctor=sidorov"
    response = client.get(url)
    assert response.status_code == 200


def test_customer_visits_page(create_specs_and_doctors_and_customers, client):
    url = reverse("customervisits")
    response = client.get(url)
    assert response.status_code == 200
