from django.urls import path
from . import views

app_name = 'financeiro'

urlpatterns = [
    path('cadastrar_usuario/', views.cadastrar_usuario_financeiro_view, name='cadastrar_usuario_financeiro'),
]
