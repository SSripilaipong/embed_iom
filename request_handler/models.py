from django.db import models


class SensorData(models.Model):
    timestamp = models.DateTimeField()
    sensor_id = models.IntegerField()
    sensor_type = models.CharField(max_length=5)  # light, humid
    value = models.FloatField()


class SensorData2(models.Model):
    timestamp = models.DateTimeField()
    sensor_id = models.IntegerField()
    light = models.FloatField()
    humid = models.FloatField()
