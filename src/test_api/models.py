from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=50)

