from django.db import models

from datetime import datetime

class FipeData(models.Model):
    year = models.IntegerField()
    fipe_id = models.IntegerField()
    maker_description = models.CharField(max_length=255)
    model_description = models.CharField(max_length=255)
    version_description = models.CharField(max_length=255)
    fuel = models.CharField(max_length=255)
    current_value = models.FloatField()

class PriceHistory(models.Model):
    fipe_data = models.ForeignKey(FipeData, on_delete=models.CASCADE, related_name='price_history')
    month_update = models.IntegerField()
    year_update = models.IntegerField()
    value = models.FloatField()
    is_prediction = models.BooleanField()

class SuivData(models.Model):
    fipe_id = models.IntegerField()
    version_id = models.IntegerField()
    version_description = models.CharField(max_length=255)
    model_id = models.IntegerField()
    model_description = models.CharField(max_length=255)
    maker_id = models.IntegerField()
    maker_description = models.CharField(max_length=255)

class Vehicle(models.Model):
    maker = models.CharField(max_length=255)
    maker_id = models.IntegerField()
    fipe_id = models.IntegerField()
    description = models.CharField(max_length=255)
    plate = models.CharField(max_length=255)
    year_model = models.IntegerField()
    year_fab = models.IntegerField()
    fuel = models.CharField(max_length=255)
    chassis = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    bodywork = models.CharField(max_length=255)
    power = models.IntegerField()
    is_national = models.BooleanField()
    axis_count = models.IntegerField()
    total_gross_weight = models.FloatField()
    maximum_traction_capacity = models.FloatField()
    cc = models.IntegerField()
    seat_count = models.IntegerField()
    load_capacity = models.FloatField()
    gear_box_number = models.CharField(max_length=255)
    back_axis_count = models.CharField(max_length=255)
    aux_axis_count = models.CharField(max_length=255)
    engine_number = models.CharField(max_length=255)

class SUIVRequest(models.Model):
    endpoint = models.CharField(max_length=255)
    date = models.DateTimeField(default=datetime.now)

