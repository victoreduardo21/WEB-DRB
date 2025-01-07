import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sqlite3

# Escopos de acesso ao Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Configurações das planilhas e intervalos
SPREADSHEET_ID_CADASTRO = "1JWO418p5HMf3cfKBWkalTD_MDPf3P5utXQqiCJXWR6M"
RANGE_CADASTRO = "Cadastro_motorista!A1:Z1000"

def get_service():
    """Autentica e retorna o serviço do Google Sheets."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("sheets", "v4", credentials=creds)
        return service
    except HttpError as err:
        print("Erro ao acessar o Google Sheets:", err)
        return None

def import_planilha_to_db(spreadsheet_id, range_name, table_name):
    """Importa dados de uma planilha para o banco de dados."""
    service = get_service()
    if not service:
        print("Erro ao autenticar com Google Sheets.")
        return

    # Obtém os dados da planilha
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get("values", [])

    if not values:
        print(f"Nenhum dado encontrado na planilha {spreadsheet_id}.")
        return

    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    # Limpa a tabela antes de inserir novos dados
    print(f"Limpando a tabela: {table_name}")
    cursor.execute(f"DELETE FROM {table_name}")

    # Obtém os cabeçalhos da planilha (primeira linha)
    headers = values[0]
    rows = values[1:]  # Exclui a linha de cabeçalhos

    # Insere cada linha no banco de dados
    for row in rows:
        try:
            placeholders = ",".join("?" for _ in headers)
            query = f"INSERT INTO {table_name} ({','.join(headers)}) VALUES ({placeholders})"
            cursor.execute(query, row)
        except Exception as e:
            print(f"Erro ao inserir dados: {row}, Erro: {e}")

    conn.commit()
    conn.close()
    print(f"Dados importados com sucesso para a tabela {table_name}.")

def main():
    # Importa os dados de cadastro
    import_planilha_to_db(SPREADSHEET_ID_CADASTRO, RANGE_CADASTRO, "cadastro_motorista")

if __name__ == "__main__":
    main()
