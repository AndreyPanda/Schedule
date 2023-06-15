import pytest
from django.contrib.auth import get_user_model
from main.models import Specialization, Doctor, Client


@pytest.fixture
def user(django_user_model):
    User = get_user_model()
    user = User.objects.create_user(
        email="1212@mail.ru", first_name="Andrey", phone="+963"
    )
    return user


# Фикстура для создания пары специализаций и пары докторов в тестовой БД
# Заодно здесь же тестируем, что запись в БД доступна
@pytest.fixture()
def create_specs_and_doctors_and_clients(user):
    spec1 = Specialization.objects.create(title="Специализация 1", slug="spec1")
    spec1.full_clean()
    spec2 = Specialization.objects.create(title="Специализация 2", slug="spec2")
    spec2.full_clean()
    doctor1 = Doctor.objects.create(
        last_name="Сидоров",
        first_name="Илья",
        fathers_name="Витальевич",
        slug="sidorov",
        specialization=spec1,
        education="Москва, 1980",
    )
    doctor1.full_clean()
    doctor2 = Doctor.objects.create(
        last_name="Петров",
        first_name="Иван",
        fathers_name="Михайлович",
        slug="petrov",
        specialization=spec2,
        education="Киров, 1985",
    )
    doctor2.full_clean()

    client1 = Client.objects.create(
        last_name="Бахметьев>",
        first_name="Андрей",
        fathers_name="Витальевич",
        birth_date="1985-05-05",
        phone="+9-123-456-8998",
    )
    client1.full_clean()

    client2 = Client.objects.create(
        last_name="Майоров",
        first_name="Ульян",
        fathers_name="Олегович",
        birth_date="1985-05-05",
        phone="+7-906-456-2020",
    )
    client2.full_clean()
