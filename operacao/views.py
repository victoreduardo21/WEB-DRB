from django.shortcuts import render, redirect
from django.contrib import messages
from core.config import get_db  # Função de conexão ao MongoDB
from django.core.serializers.json import DjangoJSONEncoder
import json

def chamadas_operacao(request):
    user_nome = request.session.get('user_nome', 'Usuário')  # Recupera o nome ou mostra 'Usuário' como padrão
    chamadas = [
        {'ID': '1', 'motorista': 'João Silva', 'cavalo': 'MDC7B81', 'carreta': 'MDC7B81', 'origem': 'Brado', 'destino': 'SANTOS BRASIL', 'horario': '13:50:00', 'obs': 'N/D', 'status': 'Pendente'},
        {'ID': '2', 'motorista': 'João Silva', 'cavalo': 'MDC7B81', 'carreta': 'MDC7B81', 'origem': 'Brado', 'destino': 'SANTOS BRASIL', 'horario': '13:50:00', 'obs': 'N/D', 'status': 'Pendente'},
    ]
    
    context = {'chamadas': chamadas, 'user': request.user}
    return render(request, 'operacao/chamadas_operacao.html', context)

def mapa(request):
    db = get_db()
    terminais_collection = db['Cadastro_Terminal']

    terminais = list(terminais_collection.find({}))

    # Converter ObjectId para string
    for terminal in terminais:
        terminal['_id'] = str(terminal['_id'])
        terminal['latitude'] = float(terminal['latitude'])
        terminal['longitude'] = float(terminal['longitude'])
        terminal['raio'] = float(terminal.get('raio', 0))  # Garantir que o raio é um float e default 0

    terminais_json = json.dumps(terminais, cls=DjangoJSONEncoder)
    
    context = {'terminais_json': terminais_json}
    return render(request, 'operacao/mapa.html', context)

def cadastrar(request):
    db = get_db()
    terminais_collection = db['Cadastro_Terminal']

    if request.method == 'POST':
        nome = request.POST.get('nome')
        cidade = request.POST.get('cidade')
        endereco = request.POST.get('endereco')
        cnpj = request.POST.get('cnpj')
        cid_rota = request.POST.get('cid_rota')
        raio = request.POST.get('raio')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Verificar duplicação (por exemplo, mesmo CNPJ)
        if terminais_collection.find_one({"cnpj": cnpj}):
            messages.error(request, "Já existe um terminal cadastrado com este CNPJ.")
        else:
            terminais_collection.insert_one({
                "nome": nome,
                "cidade": cidade,
                "endereco": endereco,
                "cnpj": cnpj,
                "cid_rota": cid_rota,
                "raio": float(raio) if raio else 0,
                "latitude": float(latitude),
                "longitude": float(longitude),
            })
            messages.success(request, "Terminal cadastrado com sucesso.")

        return redirect('operacao:cadastrar')

    terminais = list(terminais_collection.find({}))
    return render(request, 'operacao/cadastrar.html', {'terminais': terminais})
