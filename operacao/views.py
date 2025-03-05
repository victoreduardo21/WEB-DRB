from django.shortcuts import render, redirect
from django.contrib import messages
from core.config import get_db  # Função de conexão ao MongoDB
from django.core.serializers.json import DjangoJSONEncoder
import json

from core.google.models.terminal import Terminal
from core.google.worksheets import get_terminais


def chamadas_operacao(request):
    user_nome = request.session.get(
        "user_nome", "Usuário"
    )  # Recupera o nome ou mostra 'Usuário' como padrão
    chamadas = [
        {
            "ID": "1",
            "motorista": "João Silva",
            "cavalo": "MDC7B81",
            "carreta": "MDC7B81",
            "origem": "Brado",
            "destino": "SANTOS BRASIL",
            "horario": "13:50:00",
            "obs": "N/D",
            "status": "Pendente",
        },
        {
            "ID": "2",
            "motorista": "João Silva",
            "cavalo": "MDC7B81",
            "carreta": "MDC7B81",
            "origem": "Brado",
            "destino": "SANTOS BRASIL",
            "horario": "13:50:00",
            "obs": "N/D",
            "status": "Pendente",
        },
    ]

    context = {"chamadas": chamadas, "user": request.user}
    return render(request, "operacao/chamadas_operacao.html", context)


def mapa(request):
    planilha_terminais = get_terminais()
    terminais = planilha_terminais.buscar_todos_terminais()

    terminais_dict = [terminal.to_dict() for terminal in terminais]
    context = {"terminais_json": json.dumps(terminais_dict, cls=DjangoJSONEncoder)}

    return render(request, "operacao/mapa.html", context)


def cadastrar(request):
    planilha_terminais = get_terminais()
    terminais = planilha_terminais.buscar_todos_terminais()
    terminais_dict = [terminal.to_dict() for terminal in terminais]

    if request.method == "POST":
        nome = request.POST.get("nome")
        cidade = request.POST.get("cidade")
        endereco = request.POST.get("endereco")
        cnpj = request.POST.get("cnpj")
        cid_rota = request.POST.get("cid_rota")
        raio = request.POST.get("raio")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        terminais_existentes = planilha_terminais.buscar_terminais_por_cnpj(cnpj)

        if len(terminais_existentes) > 0:
            messages.error(request, "Já existe um terminal cadastrado com este CNPJ.")
        else:
            novo_terminal = Terminal(
                id=None,
                nome=nome,
                cidade=cidade,
                endereco=endereco,
                cnpj=cnpj,
                cid_rota=cid_rota,
                raio=float(raio) if raio else 0,
                entrada=(float(latitude), float(longitude)),
                saida=(0, 0),
            )

            planilha_terminais.cadastrar_terminal(novo_terminal)
            messages.success(request, "Terminal cadastrado com sucesso.")

        return redirect("operacao:cadastrar")

    context = {"terminais": terminais_dict}
    return render(request, "operacao/cadastrar.html", context)
