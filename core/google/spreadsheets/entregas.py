from typing import List, Optional
from gspread import Spreadsheet

from core.google.models.entrega import Entrega


class PlanilhaEntregas:
    def __init__(self, spreadsheet: Spreadsheet):
        """
        Inicializa a classe PlanilhaEntregas com a planilha do Google Sheets.

        Args:
            spreadsheet (Spreadsheet): Objeto da planilha do Google Sheets.
        """
        self.spreadsheet = spreadsheet
        self.worksheet = spreadsheet.worksheet(title="CADASTRO_ENTREGAS")

    def _get_valid_records(self) -> List[dict]:
        """
        Retorna os registros da planilha, ignorando colunas com cabeçalhos vazios.

        Returns:
            List[dict]: Lista de dicionários representando as linhas da planilha.
        """
        # Obtém todas as linhas da planilha
        linhas = self.worksheet.get_all_values()

        # A primeira linha é o cabeçalho
        cabecalho = linhas[1]

        # Filtra colunas com cabeçalhos não vazios
        colunas_validas = [i for i, valor in enumerate(cabecalho) if valor.strip()]

        # Processa as linhas, mantendo apenas as colunas válidas
        dados = []
        for linha in linhas[1:]:
            registro = {}
            for i in colunas_validas:
                chave = cabecalho[i]
                valor = linha[i] if i < len(linha) else ""
                registro[chave] = valor
            dados.append(registro)

        return dados

    def buscar_por_motorista(self, id_motorista: str) -> Optional[Entrega]:
        """
        Busca uma entrega pelo ID do motorista.

        Args:
            id_motorista (str): ID do motorista associado à entrega.

        Returns:
            Optional[Entrega]: Objeto Entrega encontrado, ou None se não for encontrado.
        """
        dados = self._get_valid_records()
        for entrega in dados:
            cod = entrega.get("Cod", "")
            if cod and str(cod) == str(id_motorista):
                return Entrega.from_dict(entrega)
        return None

    def buscar_todas_entregas(self) -> List[Entrega]:
        """
        Retorna uma lista de todas as entregas cadastradas na planilha.

        Returns:
            List[Entrega]: Lista de objetos Entrega.
        """
        dados = self._get_valid_records()
        entregas = []
        for entrega in dados:
            try:
                entregas.append(Entrega.from_dict(entrega))
            except (ValueError, KeyError):
                continue
        return entregas
