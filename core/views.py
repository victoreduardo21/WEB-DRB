from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from rest_framework.decorators import api_view
from .config import get_db


# View de Login
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")  # Captura o email do formulário
        senha = request.POST.get("senha")  # Captura a senha do formulário

        db = get_db()  # Obtém a conexão com o banco de dados
        cadastro_funcionario_collection = db["Cadastro_Funcionario"]  # Acessa a coleção
        user = cadastro_funcionario_collection.find_one(
            {"email": email}
        )  # Busca pelo email

        if (
            user and user["senha"] == senha
        ):  # Verifica se o email e senha estão corretos
            # Armazenar informações do usuário na sessão
            request.session["user_id"] = str(
                user["_id"]
            )  # Salva o ID do usuário na sessão
            request.session["user_nome"] = user[
                "nome"
            ]  # Salva o nome do usuário na sessão
            request.session["user_setor"] = user[
                "setor"
            ]  # Salva o setor do usuário na sessão (ex.: Operação, Administração, Financeiro)

            messages.success(
                request, "Login bem-sucedido!"
            )  # Mostra mensagem de sucesso
            return redirect("conta")  # Redireciona para a view 'conta'
        else:
            messages.error(
                request, "Email ou senha incorretos."
            )  # Mostra mensagem de erro
    return render(request, "core/login.html")


# View da Página da Conta
def conta(request):
    # Obtém as informações do usuário da sessão
    user_nome = request.session.get("user_nome", "Usuário")  # Nome do usuário
    user_setor = request.session.get("user_setor", "")  # Setor do usuário

    # Passa as informações para o contexto do template
    context = {
        "user_nome": user_nome,
        "user_setor": user_setor,
    }

    return render(request, "core/conta.html", context)


# API de Login
@api_view(["POST"])
def login_api(request):
    if request.method == "POST":
        email = request.data.get("email")  # Captura o email
        senha = request.data.get("senha")  # Captura a senha

        db = get_db()  # Obtém a conexão com o banco de dados
        cadastro_funcionario_collection = db["Cadastro_Funcionario"]  # Acessa a coleção
        user = cadastro_funcionario_collection.find_one(
            {"email": email}
        )  # Busca pelo email

        if (
            user and user["senha"] == senha
        ):  # Verifica se o email e senha estão corretos
            # Retorna as informações relevantes (ex.: setor e ID do usuário)
            return JsonResponse(
                {
                    "message": "Login successful",
                    "user_id": str(user["_id"]),
                    "user_setor": user["setor"],  # Inclui o setor na resposta da API
                }
            )
        else:
            # Retorna resposta de erro
            return JsonResponse({"message": "Invalid credentials"}, status=401)


# Middleware para verificar acesso baseado no setor
def verifica_setor(view_func):
    def wrapper(request, *args, **kwargs):
        user_setor = request.session.get(
            "user_setor"
        )  # Obtém o setor do usuário da sessão

        # Exemplo de lógica de permissão (substituir com os requisitos reais)
        if not user_setor or user_setor not in kwargs.get("permissoes", []):
            return HttpResponseForbidden(
                "Você não tem permissão para acessar esta página."
            )
        return view_func(request, *args, **kwargs)

    return wrapper
