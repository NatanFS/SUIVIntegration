from django.db import models
from django.contrib.postgres.fields import ArrayField

class Vehicle(models.Model):
    maker = models.CharField(max_length=255, null=True)
    maker_id = models.IntegerField(null=True)
    fipe_id = models.IntegerField(null=True)
    description = models.CharField(max_length=255, null=True)
    plate = models.CharField(max_length=7, null=True)
    year_model = models.PositiveIntegerField(null=True)
    year_fab = models.PositiveIntegerField(null=True)
    fuel = models.CharField(max_length=255, null=True)
    chassis = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    species = models.CharField(max_length=255, null=True)
    bodywork = models.CharField(max_length=255, null=True)
    power = models.IntegerField(null=True)
    is_national = models.BooleanField(null=True)
    axis_count = models.PositiveIntegerField(null=True)
    total_gross_weight = models.FloatField(null=True)
    maximum_traction_capacity = models.FloatField(null=True)
    cc = models.IntegerField(null=True)
    seat_count = models.PositiveIntegerField(null=True)
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
    value = models.FloatField(null=True)
    aftermarket_maker_description = models.CharField(max_length=255, null=True)

class TechnicalSpecsVehicle(models.Model):
    year = models.PositiveIntegerField(null=True)
    fipe_id = models.IntegerField(null=True)
    description = models.CharField(max_length=255)
    specs = ArrayField(
        models.JSONField(
            default=dict,
            blank=True,
        ),
        default=list,
        blank=True,
    )

class RevisionPlan(models.Model):
    year = models.IntegerField(null=True)
    version_id = models.IntegerField(null=True)
    kilometers = models.PositiveIntegerField(null=True)
    months = models.PositiveIntegerField(null=True)
    parcels = models.PositiveIntegerField(null=True)
    duration_minutes = models.PositiveIntegerField(null=True)
    full_price = models.FloatField(null=True)
    parcel_price = models.FloatField(null=True)
    changed_parts = ArrayField(
        models.JSONField(
            default=dict,
            blank=True,
        ),
        default=list,
        blank=True,
        null=True,
    )
    inspections = ArrayField(
        models.CharField(max_length=255),
        default=list,
        blank=True,
        null=True,
    )

class SummaryVehicle(models.Model):
    fipe_id = models.IntegerField(null=True)
    version_id = models.IntegerField(null=True)
    maker_description = models.CharField(max_length=255, null=True)
    model_description = models.CharField(max_length=255, null=True)
    text = models.TextField(null=True)
    image_url = models.URLField(null=True)
    maker_logo_url = models.URLField(null=True)

class Recall(models.Model):
    vehicle = models.ForeignKey(Vehicle, verbose_name=("Recalls"), on_delete=models.CASCADE, related_name="recalls")
    description = models.CharField(max_length=255)

class IPVA(models.Model):
    base_fipe_value = models.FloatField(null=True)
    state = models.CharField(max_length=50)
    value = models.FloatField(null=True)

class Equipment(models.Model):
    fipe_id = models.IntegerField(null=True)
    year = models.PositiveIntegerField(null=True)
    description = models.CharField(max_length=255, null=True)

class ComparisonData(models.Model):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    data = models.JSONField(null=True)

class SUIVRequest(models.Model):
    endpoint = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(auto_now_add=True)


