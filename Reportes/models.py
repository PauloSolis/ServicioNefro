from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.


class Reportes(models.Model):  # NEF-206
    # This model is just for the permission to view reports
    aux = models.BooleanField()
