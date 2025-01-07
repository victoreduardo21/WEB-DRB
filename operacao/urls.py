from django.urls import path
from . import views

app_name = 'operacao'

urlpatterns = [
    path('chamadas_operacao/', views.chamadas_operacao, name='chamadas_operacao'),
    path('mapa/', views.mapa, name='mapa'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
]
