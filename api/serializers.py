from rest_framework import serializers
from .models import Equipment, FipeData, Part, PriceHistory, RevisionPlan, SuivData, SummaryVehicle, TechnicalSpecsGroup, Vehicle

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

class RevisionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevisionPlan
        fields = '__all__'
class TechnicalSpecsGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSpecsGroup
        fields = '__all__'


class SummaryVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummaryVehicle
        fields = '__all__'

class SuivDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuivData
        fields = '__all__'

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'

class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ('month_update', 'year_update', 'value', 'is_prediction')

class FipeDataSerializer(serializers.ModelSerializer):
    price_history = PriceHistorySerializer(many=True, read_only=True)

    class Meta:
        model = FipeData
        fields = ('year', 'fipe_id', 'maker_description', 'model_description', 'version_description', 'fuel', 'current_value', 'price_history')

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('id', 'plate', 'year_model', 'year_fab', 'fuel', 'chassis', 'type', 'species', 'bodywork', 'power', 'is_national', 'axis_count', 'total_gross_weight', 'maximum_traction_capacity', 'gear_box_number', 'back_axis_count', 'aux_axis_count', 'engine_number', 'maker', 'maker_id', 'description', 'fipe_id', 'seat_count')
