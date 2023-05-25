from django.db import models

class Specialization(models.Model):
    title = models.CharField(max_length=255)
    visit_duration = models.IntegerField(blank=False, default=30)
    is_used = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Doctor(models.Model):
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    fathers_name = models.CharField(max_length=255)
    specialization = models.ForeignKey(Specialization, related_name="doctors_specialization", on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", null=True, blank=True)
    education = models.TextField(max_length=2000)
    description = models.TextField(max_length=5000, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    working_start_time = models.TimeField(blank=True, default='08:00')
    working_finish_time = models.TimeField(blank=True, default='17:00')
    is_active = models.BooleanField(default=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.fathers_name

