from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .config import get_db  # Importar a função para conectar ao MongoDB
import json


@csrf_exempt
@api_view(["POST"])
def login_motorista(request):
    if request.method == "POST":
        data = json.loads(request.body)
        placa = data.get("placa")
        cpf = data.get("cpf")

        db = get_db()  # Obtém a conexão com o banco de dados
        cadastro_motorista_collection = db["Cadastro_motorista"]  # Acessa a coleção
        user = cadastro_motorista_collection.find_one(
            {"placa": placa, "cpf": cpf}
        )  # Busca pela placa e CPF

        if user:  # Verifica se o usuário foi encontrado
            return JsonResponse({"status": "sucesso", "dados": {}}, status=200)
        else:
            return JsonResponse(
                {"status": "falha", "mensagem": "Credenciais inválidas"}, status=401
            )
    return JsonResponse(
        {"status": "falha", "mensagem": "Método não permitido"}, status=405
    )
