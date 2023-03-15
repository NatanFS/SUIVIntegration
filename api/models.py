from django.db import models

from datetime import datetime

class Vehicle(models.Model):
    maker = models.CharField(max_length=255, null=True)
    maker_id = models.IntegerField(null=True)
    fipe_id = models.IntegerField(null=True)
    description = models.CharField(max_length=255, null=True)
    plate = models.CharField(max_length=255, null=True)
    year_model = models.IntegerField(null=True)
    year_fab = models.IntegerField(null=True)
    fuel = models.CharField(max_length=255, null=True)
    chassis = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    species = models.CharField(max_length=255, null=True)
    bodywork = models.CharField(max_length=255, null=True)
    power = models.IntegerField(null=True)
    is_national = models.BooleanField(null=True)
    axis_count = models.IntegerField(null=True)
    total_gross_weight = models.FloatField(null=True)
    maximum_traction_capacity = models.FloatField(null=True)
    cc = models.IntegerField(null=True)
    seat_count = models.IntegerField(null=True)
    load_capacity = models.FloatField(null=True)
    gear_box_number = models.CharField(max_length=255, null=True)
    back_axis_count = models.CharField(max_length=255, null=True)
    aux_axis_count = models.CharField(max_length=255, null=True)
    engine_number = models.CharField(max_length=255, null=True)

class FipeData(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='fipe_data')
    year = models.IntegerField(null=True)
    fipe_id = models.IntegerField(null=True)
    maker_description = models.CharField(max_length=255, null=True)
    model_description = models.CharField(max_length=255, null=True)
    version_description = models.CharField(max_length=255, null=True)
    fuel = models.CharField(max_length=255, null=True)
    current_value = models.FloatField(null=True)

class PriceHistory(models.Model):
    fipe_data = models.ForeignKey(FipeData, on_delete=models.CASCADE, related_name='price_history')
    month_update = models.IntegerField(null=True)
    year_update = models.IntegerField(null=True)
    value = models.FloatField(null=True)
    is_prediction = models.BooleanField(null=True)

class SuivData(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='suiv_data')
    fipe_id = models.IntegerField(null=True)
    version_id = models.IntegerField(null=True)
    version_description = models.CharField(max_length=255, null=True)
    model_id = models.IntegerField(null=True)
    model_description = models.CharField(max_length=255, null=True)
    maker_id = models.IntegerField(null=True)
    maker_description = models.CharField(max_length=255, null=True)

class Part(models.Model):
    year = models.IntegerField(null=True)
    fipe_id = models.IntegerField(null=True)
    nickname_id = models.IntegerField(null=True)
    nickname_description = models.CharField(max_length=255, null=True)
    complement = models.CharField(max_length=255, null=True)
    part_number = models.CharField(max_length=255, null=True)
    is_genuine = models.BooleanField(null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    aftermarket_maker_description = models.CharField(max_length=255, null=True)

class SUIVRequest(models.Model):
    endpoint = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(auto_now_add=True)


