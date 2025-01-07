# backend/config.py

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def get_db():
    uri = "mongodb+srv://DRBLogistica:SolCafé123@cluster0.mhq08.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        # Enviar um ping para confirmar a conexão
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    db = client['DRB_Logística']
    return db
