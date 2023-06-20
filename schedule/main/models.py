from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


# Вспомогательный класс для управления классом User
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


# СОздали класс User вместо стандартного из поставки Django, так как нам необходимо назначить поле телефон
# и вместо username видеть email
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=20, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


class Specialization(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    visit_duration = models.IntegerField(blank=False, default=30)
    is_used = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Doctor(models.Model):
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    fathers_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    specialization = models.ForeignKey(
        Specialization,
        related_name="doctors_specialization",
        on_delete=models.SET_NULL,
        null=True,
    )
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", null=True, blank=True)
    education = models.TextField(max_length=2000)
    description = models.TextField(max_length=5000, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    working_start_time = models.TimeField(default="08:00")
    working_finish_time = models.TimeField(default="17:00")
    lunch_start_time = models.TimeField(default="12:00")
    lunch_finish_time = models.TimeField(default="13:00")
    working_days = models.IntegerField(default="1234567")
    is_active = models.BooleanField(default=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.last_name + " " + self.first_name + " " + self.fathers_name


class Customer(models.Model):
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    fathers_name = models.CharField(max_length=255, verbose_name="Отчество")
    birth_date = models.DateField(
        verbose_name="Дата рождения в формате ГГГГ-ММ-ДД", null=True
    )
    phone = models.CharField(max_length=20, verbose_name="Телефон", null=True)

    def __str__(self):
        return self.last_name + " " + self.first_name + " " + self.fathers_name


class Visit(models.Model):
    visit_datetime = models.DateTimeField()
    doctor_to_visit = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    customer_visiting = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return (
            self.visit_datetime.isoformat()
            + " к врачу "
            + self.doctor_to_visit.__repr__()
            + " записан "
            + self.customer_visiting.__repr__()
        )
