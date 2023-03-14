from django.http import JsonResponse
from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from decouple import config
from django.core import serializers
import json

from api.models import FipeData, PriceHistory, SUIVRequest, SuivData, Vehicle
from api.serializers import FipeDataSerializer, SuivDataSerializer, VehicleSerializer
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
        print("veiculo", vehicle)
        if vehicle:
            vehicle = vehicle[0]
        else:
            # Recupera dados da SUIV, caso não haja no banco de dados
            api_key = config('SUIV_API_KEY')
            endpoint = 'api/v3/VehicleInfo/byplate'
            url = f'https://api.suiv.com.br/{endpoint}?plate={plate}&key={api_key}'
            response = requests.get(url)

            if not response.ok:
                return Response({'error': 'Fail retrieving data'}, status=500)

            print("Fez request à SUIV")
            
            # Registra chamada à SUIV
            register_suiv_request(endpoint)

            # Salva dados no banco
            if response.status_code == 200:
            # if True:
                # data = None
                # with open('data/prisma.json') as f:
                #     data = json.load(f)
                #     print("dados carregados")
                data = response.json()
                vehicle, suiv_data_objects, fipe_data_objects = save_suiv_data(data)

        json_data = generate_vehicle_info_json(vehicle, suiv_data_objects, fipe_data_objects)

        # json_data = json.dumps(data)

        return JsonResponse(json_data, safe=False)

def generate_vehicle_info_json(vehicle, fipe_data_objects, suiv_data_objects):
    # Serializa dados em JSON
    vehicle_data = VehicleSerializer(vehicle).data
    fipe_data_collection = FipeDataSerializer(vehicle.fipe_data.all(), many=True).data
    suiv_data_collection = SuivDataSerializer(vehicle.suiv_data.all(), many=True).data

    # Create the final JSON object
    
    data = {
        **vehicle_data,
        "fipeDataCollection": fipe_data_collection,
        "suivDataCollection": suiv_data_collection,
        "suivRequestCount": len(SUIVRequest.objects.all())
    }

    return data

def register_suiv_request(endpoint):
    SUIVRequest.objects.create(endpoint=endpoint)

def save_suiv_data(data):
    fipe_data_collection = data.get('fipeDataCollection', [])
    suiv_data_collection = data.get('suivDataCollection', [])
    vehicle_data = {k: v for k, v in data.items() if k not in ['fipeDataCollection', 'suivDataCollection']}

    # Instancia veículo
    vehicle = save_vehicle_data_object(vehicle_data)

    # Intancia objetos FipeData 
    fipe_data_objects = save_fipe_data_objects(fipe_data_collection, vehicle)

    # Intancia objetos PriceHistory 
    save_price_history_data_objects(fipe_data_collection)

    # Intancia objetos SuivData
    suiv_data_objects = save_suiv_data_objects(suiv_data_collection, vehicle)

    return (vehicle, suiv_data_objects, fipe_data_objects)

def save_fipe_data_objects(fipe_data_collection, vehicle):
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
            'vehicle': vehicle
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

def save_suiv_data_objects(suiv_data_collection, vehicle):
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
            'vehicle': vehicle
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
        'engine_number': vehicle_data['engineNumber'],
        'maker': vehicle_data['maker'],
        'maker_id': vehicle_data['makerId'],
        'description': vehicle_data['description'],
        'fipe_id': vehicle_data['fipeId'],
        'seat_count': vehicle_data['seatCount']
    }

    vehicle = Vehicle(**vehicle_kwargs)
    vehicle.save()
    return vehicle