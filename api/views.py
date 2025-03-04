from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from core.google.worksheets import get_motoristas
import json


@csrf_exempt
@api_view(["POST"])
def login_motorista(request):
    if request.method == "POST":
        data = json.loads(request.body)
        placa = data.get("placa")
        cpf = data.get("cpf")

        motoristas = get_motoristas()
        motorista = motoristas.buscar_motorista(cpf, placa)

        if motorista:
            return JsonResponse({"status": "sucesso", "dados": {}}, status=200)
        else:
            return JsonResponse(
                {"status": "falha", "mensagem": "Credenciais inválidas"}, status=401
            )
    return JsonResponse(
        {"status": "falha", "mensagem": "Método não permitido"}, status=405
    )
