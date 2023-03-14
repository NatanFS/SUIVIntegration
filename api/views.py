from django.http import JsonResponse
from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from decouple import config
from django.core import serializers
import json

from api.models import FipeData, PriceHistory, SUIVRequest, SuivData, Vehicle
# Create your views here.
class InformacoesVeiculoView(APIView):
    def get(self, request, *args, **kwargs):
        plate = request.GET.get('placa')
        if not plate:
            return Response({'error': 'Plate not informed'}, status=400)

        # Remove hífen da placa
        plate = plate.replace('-', '')

        # Procura dados no banco
        suiv_data_objects = None
        fipe_data_objects = None
        vehicle = Vehicle.objects.filter(plate=plate)
        if vehicle:
            vehicle = vehicle[0]
            suiv_data_objects = SuivData.objects.filter(fipe_id=vehicle.fipe_id)
            fipe_data_objects = FipeData.objects.filter(fipe_id=vehicle.fipe_id)
        else:
            # Recupera dados da SUIV, caso não haja no banco de dados
            api_key = config('SUIV_API_KEY')
            endpoint = 'api/v3/VehicleInfo/byplate'
            url = f'https://api.suiv.com.br/{endpoint}?plate={plate}&key={api_key}'
            response = requests.get(url)

            # Registra chamada à SUIV
            register_suiv_request(endpoint)

            if not response.ok:
                return Response({'error': 'Fail retrieving data'}, status=500)

            # Salva dados no banco
            if response.status_code == 200:
                data = response.json()
                vehicle, suiv_data_objects, fipe_data_objects = save_suiv_data(data)

        json_data = generate_vehicle_info_json(vehicle, suiv_data_objects, fipe_data_objects)

        return JsonResponse(json_data)

def generate_vehicle_info_json(vehicle, fipe_data_objects, suiv_data_objects):
    # Serializa dados em JSON
    vehicle_data = serializers.serialize('json', [vehicle])
    fipe_data_collection = serializers.serialize('json', fipe_data_objects, \
    use_natural_foreign_keys=True, relations={'price_history': {'use_natural_primary_keys': True}})
    suiv_data_collection = serializers.serialize('json', suiv_data_objects)

    # Convert JSON strings into Python dictionaries
    vehicle_data = json.loads(vehicle_data)[0]['fields']
    fipe_data_collection = json.loads(fipe_data_collection)
    suiv_data_collection = json.loads(suiv_data_collection)

    # Create the final JSON object
    data = {
        **vehicle_data,
        "fipeDataCollection": fipe_data_collection,
        "suivDataCollection": suiv_data_collection
    }

    # 
    json_data = json.dumps(data)
    return json_data

def register_suiv_request(endpoint):
    SUIVRequest.objects.create(endpoint=endpoint)

def save_suiv_data(data):
    fipe_data_collection = data.get('fipeDataCollection', [])
    suiv_data_collection = data.get('suivDataCollection', [])
    vehicle_data = {k: v for k, v in data.items() if k not in ['fipeDataCollection', 'suivDataCollection']}

    # Intancia objetos FipeData 
    fipe_data_objects = save_fipe_data_objects(fipe_data_collection)

    # Intancia objetos PriceHistory 
    save_price_history_data_objects(fipe_data_collection)

    # Intancia objetos SuivData
    suiv_data_objects = save_suiv_data(suiv_data_collection)

    # Instancia veículo
    vehicle = save_vehicle_data_object(vehicle_data)

    return (vehicle, suiv_data_objects, fipe_data_objects)

def save_fipe_data_objects(fipe_data_collection):
    fipe_data_objects = []
    for fipe_data in fipe_data_collection:
        fd_kwargs = {
            'year': fipe_data['year'],
            'fipe_id': fipe_data['fipeId'],
            'maker_description': fipe_data['makerDescription'],
            'model_description': fipe_data['modelDescription'],
            'version_description': fipe_data['versionDescription'],
            'fuel': fipe_data['fuel'],
            'current_value': fipe_data['currentValue'],
        }
        fipe_data_objects.append(FipeData(**fd_kwargs))
    return FipeData.objects.bulk_create(fipe_data_objects)

def save_price_history_data_objects(fipe_data_collection):
    price_history_objects = []
    for fipe_data in fipe_data_collection:
        fipe_data_obj = FipeData.objects.get(fipe_id=fipe_data['fipeId'])
        for price_history in fipe_data['priceHistory']:
            ph_kwargs = {
                'month_update': price_history['monthUpdate'],
                'year_update': price_history['yearUpdate'],
                'value': price_history['value'],
                'is_prediction': price_history['isPrediction'],
                'fipe_data': fipe_data_obj,
            }
            price_history_objects.append(PriceHistory(**ph_kwargs))
    return PriceHistory.objects.bulk_create(price_history_objects)

def save_suiv_data_objects(suiv_data_collection):
    suiv_data_objects = []
    for suiv_data in suiv_data_collection:
        sd_kwargs = {
            'fipe_id': suiv_data['fipeId'],
            'version_id': suiv_data['versionId'],
            'version_description': suiv_data['versionDescription'],
            'model_id': suiv_data['modelId'],
            'model_description': suiv_data['modelDescription'],
            'maker_id': suiv_data['makerId'],
            'maker_description': suiv_data['makerDescription'],
        }
        suiv_data_objects.append(SuivData(**sd_kwargs))
    return SuivData.objects.bulk_create(suiv_data_objects)


def save_vehicle_data_object(vehicle_data):
    vehicle_kwargs = {
        'plate': vehicle_data['plate'],
        'year_model': vehicle_data['yearModel'],
        'year_fab': vehicle_data['yearFab'],
        'fuel': vehicle_data['fuel'],
        'chassis': vehicle_data['chassis'],
        'type': vehicle_data['type'],
        'species': vehicle_data['species'],
        'bodywork': vehicle_data['bodywork'],
        'power': vehicle_data['power'],
        'is_national': vehicle_data['isNational'],
        'axis_count': vehicle_data['axisCount'],
        'total_gross_weight': vehicle_data['totalGrossWeight'],
        'maximum_traction_capacity': vehicle_data['maximumTractionCapacity'],
        'gear_box_number': vehicle_data['maximumTractionCapacity'],
        'back_axis_count': vehicle_data['backAxisCount'],
        'aux_axis_count': vehicle_data['auxAxisCount'],
        'engine_number': vehicle_data['engineNumber']
    }

    vehicle = Vehicle(**vehicle_kwargs)
    vehicle.save()
    return vehicle