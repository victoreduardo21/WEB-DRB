from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login_motorista/', methods=['POST'])
def login_motorista():
    data = request.get_json()
    placa = data.get('placa')
    cpf = data.get('cpf')

    # Aqui você deve fazer a verificação dos dados no banco de dados.
    # Vou usar um exemplo simples de verificação:
    if placa == 'ABC1234' and cpf == '12345678901':
        return jsonify({'status': 'sucesso', 'dados': {}}), 200
    else:
        return jsonify({'status': 'falha', 'mensagem': 'Credenciais inválidas'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
