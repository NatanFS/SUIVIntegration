import json
from django.http import JsonResponse
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from decouple import config
from api.models import Equipment, Part, RevisionPlan, SUIVRequest, SummaryVehicle, TechnicalSpecsGroup, Vehicle
from api.serializers import EquipmentSerializer, RevisionPlanSerializer, SummaryVehicleSerializer, TechnicalSpecsGroupSerializer
from api.utils import generate_basic_pack_info, generate_vehicle_info_json, register_suiv_request, save_equipments, save_parts_data_object, save_revision_plans, save_suiv_data, save_summary_data_object, save_technical_specs_groups

# Create your views here.


class VehicleInfoView(APIView):
    def get(self, request, *args, **kwargs):
        plate = request.GET.get('plate')
        if not plate:
            return Response({'error': 'Plate not informed'}, status=400)

        # Remove hífen da placa
        plate = plate.replace('-', '')
        plate = plate.upper()

        # Procura dados no banco
        vehicle = Vehicle.objects.filter(plate=plate)
        print("veiculo", vehicle)
        if vehicle:
            vehicle = vehicle[0]
        else:
            # Recupera dados da SUIV, caso não haja no banco de dados
            api_key = config('SUIV_API_KEY')
            endpoint = '/api/v3/VehicleInfo/byplate'
            url = f'https://api.suiv.com.br{endpoint}?key={api_key}&plate={plate}'

            inputs = {
                "plate": plate,
            }

            # Verifica se já houve requisição para o mesmo endpoint, com os mesmos inputs
            suiv_requests = SUIVRequest.objects.filter(
                endpoint=endpoint, inputs__contains=inputs)
            if suiv_requests:
                return Response({'error': 'Data not informed'}, status=404)

            response = requests.get(url)

            if response.status_code == 404 or response.status_code == 401:
                register_suiv_request(endpoint, inputs=inputs)
                return Response({'error': 'Data not found'}, status=404)

            if not response.ok:
                return Response({'error': 'Fail retrieving data'}, status=500)
            
            register_suiv_request(endpoint, inputs=inputs)

            # Salva dados no banco
            if response.status_code == 200:
                data = response.json()
                vehicle = save_suiv_data(data)

        json_data = generate_vehicle_info_json(vehicle)
        return JsonResponse(json_data, safe=False)


class BasicPackView(APIView):
    def get(self, request, *args, **kwargs):
        year = request.GET.get('year')
        fipe_id = request.GET.get('fipeId')

        if not year:
            return Response({'error': 'Year not informed'}, status=400)
        if not fipe_id:
            return Response({'error': 'FipeId not informed'}, status=400)

        # Procura dados no banco
        parts = Part.objects.filter(year=year, fipe_id=fipe_id)

        if not parts:
            # Recupera dados da SUIV, caso não haja no banco de dados
            api_key = config('SUIV_API_KEY')
            endpoint = '/api/v3/BasicPack'
            url = f'https://api.suiv.com.br{endpoint}?key={api_key}&year={year}&fipeId={fipe_id}'

            inputs = {
                "year": year,
                "fipeId": fipe_id
            }

            # Verifica se já houve requisição para o mesmo endpoint, com os mesmos inputs
            suiv_requests = SUIVRequest.objects.filter(
                endpoint=endpoint, inputs__contains=inputs)
            if suiv_requests:
                return Response({'error': 'Data not informed'}, status=404)

            response = requests.get(url)

            if response.status_code == 404 or response.status_code == 401:
                register_suiv_request(endpoint, inputs=inputs)
                return Response({'error': 'Data not found'}, status=404)

            if not response.ok:
                return Response({'error': 'Fail retrieving data'}, status=500)
            
            register_suiv_request(endpoint, inputs=inputs)

            # Salva dados no banco
            if response.status_code == 200:
                data = response.json()
                print("Salvando objetos")
                print(data)

                parts = save_parts_data_object(data, year, fipe_id)

        json_data = generate_basic_pack_info(parts)
        return JsonResponse(json_data, safe=False)


class SummaryView(APIView):
    def get(self, request, *args, **kwargs):
        fipe_id = request.GET.get('fipeId')

        if not fipe_id:
            return Response({'error': 'FipeId not informed'}, status=400)

        # Procura dados no banco
        summary = SummaryVehicle.objects.filter(fipe_id=fipe_id)

        if summary:
            summary = summary[0]
        else:
            # Recupera dados da SUIV, caso não haja no banco de dados
            api_key = config('SUIV_API_KEY')
            endpoint = '/api/v3/Summary/byfipe'
            url = f'https://api.suiv.com.br{endpoint}?key={api_key}&fipeId={fipe_id}'

            inputs = {
                "fipeId": fipe_id
            }

            # Verifica se já houve requisição para o mesmo endpoint, com os mesmos inputs
            suiv_requests = SUIVRequest.objects.filter(
                endpoint=endpoint, inputs__contains=inputs)
            if suiv_requests:
                return Response({'error': 'Data not informed'}, status=404)

            response = requests.get(url)

            if response.status_code == 404 or response.status_code == 401:
                register_suiv_request(endpoint, inputs=inputs)
                return Response({'error': 'Data not found'}, status=404)

            if not response.ok:
                return Response({'error': 'Fail retrieving data'}, status=500)
            
            register_suiv_request(endpoint, inputs=inputs)

            # Salva dados no banco
            if response.status_code == 200:
                data = response.json()
                print("Salvando objetos")
                print(data)

                summary = save_summary_data_object(data, fipe_id)

        json_data = SummaryVehicleSerializer(summary).data
        return JsonResponse(json_data, safe=False)


class TechnicalSpecsByPlateView(APIView):
    def get(self, request, *args, **kwargs):
        plate = request.GET.get('plate')

        if not plate:
            return Response({'error': 'Plate not informed'}, status=400)

        # Procura dados no banco
        technical_specs_groups = TechnicalSpecsGroup.objects.filter(
            plate=plate)

        if not technical_specs_groups:
            # Recupera dados da SUIV, caso não haja no banco de dados
            api_key = config('SUIV_API_KEY')
            endpoint = '/api/v3/TechnicalSpecs/byplate'
            url = f'https://api.suiv.com.br{endpoint}?key={api_key}&plate={plate}'

            inputs = {
                "plate": plate
            }

            # Verifica se já houve requisição para o mesmo endpoint, com os mesmos inputs
            suiv_requests = SUIVRequest.objects.filter(
                endpoint=endpoint, inputs__contains=inputs)
            if suiv_requests:
                return Response({'error': 'Data not informed'}, status=404)

            response = requests.get(url)

            if response.status_code == 404 or response.status_code == 401:
                register_suiv_request(endpoint, inputs=inputs)
                return Response({'error': 'Data not found'}, status=404)

            if not response.ok:
                return Response({'error': 'Fail retrieving data'}, status=500)
            
            register_suiv_request(endpoint, inputs=inputs)

            # Salva dados no banco
            if response.status_code == 200:
                data = response.json()
                print("Salvando objetos")
                print(data)

                technical_specs_groups = save_technical_specs_groups(
                    data, plate)

        json_data = TechnicalSpecsGroupSerializer(
            technical_specs_groups, many=True).data
        return JsonResponse(json_data, safe=False)


class RevisionPlanView(APIView):
    def get(self, request, *args, **kwargs):
        version_id = request.GET.get('versionId')
        year = request.GET.get('year')

        if not version_id:
            return Response({'error': 'versionId not informed'}, status=400)
        if not year:
            return Response({'error': 'year not informed'}, status=400)

        # Procura dados no banco
        revision_plans = RevisionPlan.objects.filter(
            version_id=version_id, year=year)

        if not revision_plans:
            # Recupera dados da SUIV, caso não haja no banco de dados
            api_key = config('SUIV_API_KEY')
            endpoint = '/api/v3/RevisionPlan'
            url = f'https://api.suiv.com.br{endpoint}?key={api_key}&versionId={version_id}&year={year}'

            inputs = {
                "versionId": version_id,
                "year": year
            }
            
            # Verifica se já houve requisição para o mesmo endpoint, com os mesmos inputs
            suiv_requests = SUIVRequest.objects.filter(
                endpoint=endpoint, inputs__contains=inputs)
            if suiv_requests:
                return Response({'error': 'Data not informed'}, status=404)

            response = requests.get(url)

            if response.status_code == 404 or response.status_code == 401:
                register_suiv_request(endpoint, inputs=inputs)
                return Response({'error': 'Data not found'}, status=404)

            if not response.ok:
                return Response({'error': 'Fail retrieving data'}, status=500)
            
            register_suiv_request(endpoint, inputs=inputs)

            # Salva dados no banco
            if response.status_code == 200:
                data = response.json()
                print("Salvando objetos")
                print(data)

                revision_plans = save_revision_plans(data,
                                                     version_id=version_id, year=year)

        json_data = RevisionPlanSerializer(revision_plans, many=True).data
        return JsonResponse(json_data, safe=False)


class EquipmentsView(APIView):
    def get(self, request, *args, **kwargs):
        fipe_id = request.GET.get('fipeId')
        year = request.GET.get('year')

        if not fipe_id:
            return Response({'error': 'fipeId not informed'}, status=400)
        if not year:
            return Response({'error': 'year not informed'}, status=400)

        # Procura dados no banco
        equipments = Equipment.objects.filter(fipe_id=fipe_id, year=year)

        if not equipments:
            # Recupera dados da SUIV, caso não haja no banco de dados
            api_key = config('SUIV_API_KEY')
            endpoint = '/api/v3/Equipments'
            url = f'https://api.suiv.com.br{endpoint}?key={api_key}&fipeId={fipe_id}&year={year}'

            inputs = {
                "fipeId": fipe_id,
                "year": year
            }

            # Verifica se já houve requisição para o mesmo endpoint, com os mesmos inputs
            suiv_requests = SUIVRequest.objects.filter(
                endpoint=endpoint, inputs__contains=inputs)
            if suiv_requests:
                return Response({'error': 'Data not informed'}, status=404)

            response = requests.get(url)

            if response.status_code == 404 or response.status_code == 401:
                register_suiv_request(endpoint, inputs=inputs)
                return Response({'error': 'Data not found'}, status=404)

            if not response.ok:
                return Response({'error': 'Fail retrieving data'}, status=500)
            
            register_suiv_request(endpoint, inputs=inputs)

            # Salva dados no banco
            if response.status_code == 200:
                data = response.json()
                print("Salvando objetos")
                print(data)

                equipments = save_equipments(data,
                                             fipe_id=fipe_id, year=year)

        json_data = EquipmentSerializer(equipments, many=True).data
        return JsonResponse(json_data, safe=False)

class SuivRequestsCountView(APIView):
    def get(self, request, *args, **kwargs):
        data = {"count": len(SUIVRequest.objects.all())}
        return JsonResponse(data, safe=False)
