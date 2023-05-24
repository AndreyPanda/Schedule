from django.db import models

class Specialization(models.Model):
    title = models.CharField(max_length=255)
    visit_duration = models.IntegerField(blank=False, default=30)
    is_used = models.BooleanField(default=True)

    # def __str__(self):
    #     return self.title
