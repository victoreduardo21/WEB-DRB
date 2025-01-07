from django.shortcuts import render, redirect
from django.contrib import messages
from core.config import get_db  # Importar função para conectar ao MongoDB

def cadastrar_usuario_financeiro_view(request):
    db = get_db()
    cadastro_funcionario_collection = db['Cadastro_Funcionario']  # Acessa a coleção correta

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        setor = request.POST.get('setor')

        if cadastro_funcionario_collection.find_one({"email": email}):
            messages.error(request, "Usuário já existe.")
        else:
            cadastro_funcionario_collection.insert_one({
                "email": email,
                "senha": senha,
                "nome": nome,
                "telefone": telefone,
                "setor": setor
            })
            messages.success(request, "Usuário cadastrado com sucesso.")
            return redirect('financeiro:cadastrar_usuario_financeiro')

    # Buscar todos os usuários para exibir na tabela
    usuarios = list(cadastro_funcionario_collection.find({}))

    return render(request, 'financeiro/cadastrar_usuario.html', {'usuarios': usuarios})
