from django.urls import path
from . import views

urlpatterns = [
    path('InformacoesVeiculo/porplaca', views.InformacoesVeiculoView.as_view(), name='pesquisar-veiculo'),  
    path('PacoteBasico/', views.PacoteBasicoView.as_view(), name='pacote-basico'),  
]
