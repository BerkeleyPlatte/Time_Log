from django.db import models
from .activity import Activity
from django.urls import reverse



class Time_Allocation(models.Model):

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    start_time = models.CharField(max_length=50, null=True)
    stop_time = models.CharField(max_length=50, null=True)
    date = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("Time_Allocation")
        verbose_name_plural = ("Time_Allocations")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Time_Allocation_detail", kwargs={"pk": self.pk})
