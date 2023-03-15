from django.http import JsonResponse
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from decouple import config
from api.models import Vehicle
from api.utils import generate_vehicle_info_json, register_suiv_request, save_suiv_data

# Create your views here.
class InformacoesVeiculoView(APIView):
    def get(self, request, *args, **kwargs):
        plate = request.GET.get('placa')
        if not plate:
            return Response({'error': 'Plate not informed'}, status=400)

        # Remove hífen da placa
        plate = plate.replace('-', '')

        # Procura dados no banco
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
                data = response.json()
                vehicle = save_suiv_data(data)

        json_data = generate_vehicle_info_json(vehicle)
        return JsonResponse(json_data, safe=False)

