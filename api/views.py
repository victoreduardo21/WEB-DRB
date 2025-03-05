from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

from core.google.worksheets import get_entregas, get_motoristas
import json


@api_view(["POST"])
def login_motorista(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            placa = data.get("placa")
            cpf = data.get("cpf")

            if not placa or not cpf:
                return JsonResponse(
                    {"status": "falha", "mensagem": "Placa e CPF são obrigatórios"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            motoristas = get_motoristas()
            entregas = get_entregas()

            motorista = motoristas.buscar_motorista(cpf, placa)

            if not motorista:
                return JsonResponse(
                    {"status": "falha", "mensagem": "Credenciais inválidas"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            entrega = entregas.buscar_por_motorista(id_motorista=motorista.id)

            if not entrega:
                return JsonResponse(
                    {
                        "status": "falha",
                        "mensagem": "Motorista não possui entregas para hoje",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            return JsonResponse(
                {"status": "sucesso", "dados": entrega.to_dict()},
                status=status.HTTP_200_OK,
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "falha", "mensagem": "JSON inválido"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return JsonResponse(
                {"status": "falha", "mensagem": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return JsonResponse(
        {"status": "falha", "mensagem": "Método não permitido"},
        status=status.HTTP_405_METHOD_NOT_ALLOWED,
    )
