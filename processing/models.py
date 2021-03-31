from django.db import models


class Runway(models.Model):
  airport = models.CharField(max_length=4)
  designator = models.CharField(max_length=3)
  category = models.CharField(max_length=5)

class Airport(models.Model):
  icao = models.CharField(max_length=4)
  purpose = models.CharField(max_length=4)

class Notam(models.Model):
  notam_id = models.CharField(max_length=15)
  airport = models.CharField(max_length=4)
  qcode = models.CharField(max_length=4)
  message = models.CharField(max_length=511)
  startdate = models.DateTimeField()
  enddate = models.DateTimeField()
  comment = models.CharField(max_length=511, default="")