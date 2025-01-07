from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

def get_db():
    uri = "mongodb+srv://DRBLogistica:SolCafé123@cluster0.mhq08.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['DRB_Logística']
    return db

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    cpf = data.get('cpf')
    placa = data.get('placa')
    db = get_db()
    collection = db['motoristas']
    
    user = collection.find_one({'cpf': cpf, 'placa': placa})
    
    if user:
        return jsonify({'message': 'Login bem-sucedido'}), 200
    return jsonify({'message': 'Credenciais inválidas'}), 401

if __name__ == '__main__':
    app.run(debug=True)
