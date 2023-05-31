from django.db import models


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
    working_start_time = models.TimeField(default='08:00')
    working_finish_time = models.TimeField(default='17:00')
    lunch_start_time = models.TimeField(default='12:00')
    lunch_finish_time = models.TimeField(default='13:00')
    working_days = models.IntegerField(default='1234567')
    is_active = models.BooleanField(default=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.fathers_name


class Client(models.Model):
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    fathers_name = models.CharField(max_length=255, verbose_name='Отчество')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Телефон')

    def __str__(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.fathers_name


class Visit(models.Model):
    visit_datetime = models.DateTimeField()
    doctor_to_visit = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    client_visiting = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.visit_datetime.isoformat() + ' к врачу ' + self.doctor_to_visit.__repr__() + ' записан ' + self.client_visiting.__repr__()
