import pytest

from main.forms import AddCustomer, RegisterUserForm
from main.models import Customer, User


@pytest.mark.django_db
class TestAddCustomerForm:
    common_test_data = {
        "last_name": "Иванов-Храпунов",
        "first_name": "Антон",
        "fathers_name": "Рюрикович",
        "birth_date": "1983-01-01",
        "phone": "+1234567890",
    }

    def test_form_is_valid(self):
        test_data = self.common_test_data.copy()
        form = AddCustomer(data=test_data)
        assert form.is_valid()
        form.save()
        assert Customer.objects.count() == 1
        assert Customer.objects.last().last_name == "Иванов-Храпунов"

    def test_last_name_invalid(self):
        test_data = self.common_test_data.copy()
        test_data["last_name"] = "Ivanov"
        form = AddCustomer(data=test_data)
        assert not form.is_valid()
        assert "last_name" in form.errors
        for i in self.common_test_data.keys():
            if i != "last_name":
                assert i not in form.errors

    def test_first_name_invalid(self):
        test_data = self.common_test_data.copy()
        test_data["first_name"] = "Anton"
        form = AddCustomer(data=test_data)
        assert not form.is_valid()
        assert "first_name" in form.errors
        for i in self.common_test_data.keys():
            if i != "first_name":
                assert i not in form.errors

    def test_fathers_name_invalid(self):
        test_data = self.common_test_data.copy()
        test_data["fathers_name"] = "Рюрикович1"
        form = AddCustomer(data=test_data)
        assert not form.is_valid()
        assert "fathers_name" in form.errors
        for i in self.common_test_data.keys():
            if i != "fathers_name":
                assert i not in form.errors

    def test_birth_date_invalid_format(self):
        test_data = self.common_test_data.copy()
        test_data["birth_date"] = "12-12-1956"
        form = AddCustomer(data=test_data)
        assert not form.is_valid()
        assert "birth_date" in form.errors
        for i in self.common_test_data.keys():
            if i != "birth_date":
                assert i not in form.errors

    def test_phone_invalid_too_long(self):
        test_data = self.common_test_data.copy()
        test_data["phone"] = "+9-98989898989989898989898"
        form = AddCustomer(data=test_data)
        assert not form.is_valid()
        assert "phone" in form.errors
        for i in self.common_test_data.keys():
            if i != "phone":
                assert i not in form.errors

    def test_phone_invalid_contains_letters(self):
        test_data = self.common_test_data.copy()
        test_data["phone"] = "+9-abcd"
        form = AddCustomer(data=test_data)
        assert not form.is_valid()
        assert "phone" in form.errors
        for i in self.common_test_data.keys():
            if i != "phone":
                assert i not in form.errors


@pytest.mark.django_db
class TestRegisterUserForm:
    common_test_data = {
        "email": "123@mail.ru",
        "password": "test_password",
        "first_name": "Антон",
        "phone": "+1234567890",
    }

    def test_form_is_valid(self):
        test_data = self.common_test_data.copy()
        form = RegisterUserForm(data=test_data)
        assert form.is_valid()
        form.save()
        assert User.objects.count() == 1
        assert User.objects.last().email == "123@mail.ru"

    def test_email_invalid_without_dog(self):
        test_data = self.common_test_data.copy()
        test_data["email"] = "123mail.ru"
        form = RegisterUserForm(data=test_data)
        assert not form.is_valid()
        assert "email" in form.errors
        for i in self.common_test_data.keys():
            if i != "email":
                assert i not in form.errors

    def test_email_invalid_without_dot(self):
        test_data = self.common_test_data.copy()
        test_data["email"] = "123@mailru"
        form = RegisterUserForm(data=test_data)
        assert not form.is_valid()
        assert "email" in form.errors
        for i in self.common_test_data.keys():
            if i != "email":
                assert i not in form.errors

    def test_first_name_invalid(self):
        test_data = self.common_test_data.copy()
        test_data["first_name"] = "Anton"
        form = RegisterUserForm(data=test_data)
        assert not form.is_valid()
        assert "first_name" in form.errors
        for i in self.common_test_data.keys():
            if i != "first_name":
                assert i not in form.errors

    def test_phone_invalid_too_long(self):
        test_data = self.common_test_data.copy()
        test_data["phone"] = "+9-98989898989989898989898"
        form = RegisterUserForm(data=test_data)
        assert not form.is_valid()
        assert "phone" in form.errors
        for i in self.common_test_data.keys():
            if i != "phone":
                assert i not in form.errors

    def test_phone_invalid_contains_letters(self):
        test_data = self.common_test_data.copy()
        test_data["phone"] = "+9-abcd"
        form = RegisterUserForm(data=test_data)
        assert not form.is_valid()
        assert "phone" in form.errors
        for i in self.common_test_data.keys():
            if i != "phone":
                assert i not in form.errors
