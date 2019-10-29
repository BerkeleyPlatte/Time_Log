from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class Activity(models.Model):

    app_user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = ("Activity")
        verbose_name_plural = ("Activitys")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Activity_detail", kwargs={"pk": self.pk})
