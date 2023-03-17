from django.urls import path
from . import views

urlpatterns = [
    path('VehicleInfo/byplate', views.VehicleInfoView.as_view(), name='vehicle-info'),  
    path('BasicPack/', views.BasicPackView.as_view(), name='basic-pack'),  
    path('Summary/byfipe', views.SummaryView.as_view(), name='summary'),
    path('TechnicalSpecs/', views.TechnicalSpecsByPlateView.as_view(), name='tech-specs'), 
    path('RevisionPlan/', views.RevisionPlanView.as_view(), name='revision-plans'), 
    path('Equipments/', views.EquipmentsView.as_view(), name='equipments'),
    path('SuivRequestsCount/', views.SuivRequestsCountView.as_view(), name='suiv-counter'), 
]
