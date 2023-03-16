from django.urls import path
from . import views

urlpatterns = [
    path('VehicleInfo/byplate', views.VehicleInfoView.as_view(), name='vehicle-info'),  
    path('BasicPack/', views.BasicPackView.as_view(), name='basic-pack'),  
]
