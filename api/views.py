from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from decouple import config
# Create your views here.
class InformacoesVeiculoView(APIView):
    def get(self, request, *args, **kwargs):
        placa = request.GET.get('placa')
        if not placa:
            return Response({'error': 'Placa não informada'}, status=400)
        placa = placa.replace('-', '')

        api_key = config('SUIV_API_KEY')
        print(api_key)
        # url = f'https://api.example.com/vehicle-info?plate={placa}'
        # response = requests.get(url)
        # if not response.ok:
        #     return Response({'error': 'Falha ao recuperar dados'}, status=500)

        return Response({"message": "success"})