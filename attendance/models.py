from statistics import mode
from django.db import models

# Create your models here.
class EnrollStudent(models.Model):
    name = models.CharField(
        max_length=40, blank=False,
        null=False
    )
    sid = models.CharField(
        max_length=10,blank=False,
        null=False
    )
    emailId = models.EmailField(
        blank=False,null=False
    )
    img = models.ImageField(height_field=512,width_field=512)

    def __str__(self) -> str:
        return self.name