from gspread import Spreadsheet
from typing import List
import re

from operacao.models import Terminal


class PlanilhaTerminais:
    def __init__(self, spreadsheet: Spreadsheet):
        """
        Inicializa a classe PlanilhaTerminais com a planilha do Google Sheets.

        Args:
            spreadsheet (Spreadsheet): Objeto da planilha do Google Sheets.
        """
        self.spreadsheet = spreadsheet
        self.worksheet = spreadsheet.worksheet(title="CADASTRO_TERMINAIS")

    def _gerar_proximo_id(self) -> int:
        """
        Gera o próximo ID disponível para um novo terminal.

        Returns:
            int: Próximo ID disponível.
        """
        dados = self.worksheet.get_all_records()
        if not dados:
            return 1
        ids = [int(terminal.get("ID_TERMINAL", 0)) for terminal in dados]
        return max(ids) + 1

    def _limpar_cnpj(self, cnpj: str) -> str:
        """
        Remove máscaras (pontos, barras e hífens) do CNPJ.

        Args:
            cnpj (str): CNPJ a ser limpo.

        Returns:
            str: CNPJ sem máscaras.
        """
        return re.sub(r"[^0-9]", "", cnpj)

    def buscar_todos_terminais(self) -> List[Terminal]:
        """
        Retorna uma lista de todos os terminais cadastrados na planilha.

        Returns:
            List[Terminal]: Lista de objetos Terminal.
        """
        dados = self.worksheet.get_all_records()
        return [Terminal.from_dict(terminal) for terminal in dados]

    def buscar_terminais_por_cnpj(self, cnpj: str) -> List[Terminal]:
        """
        Retorna uma lista de terminais que possuem o CNPJ especificado.

        Args:
            cnpj (str): CNPJ a ser buscado.

        Returns:
            List[Terminal]: Lista de objetos Terminal com o CNPJ correspondente.
        """
        cnpj_limpo = self._limpar_cnpj(cnpj)
        dados = self.worksheet.get_all_records()
        return [
            Terminal.from_dict(terminal)
            for terminal in dados
            if self._limpar_cnpj(terminal.get("CNPJ", "")) == cnpj_limpo
        ]

    def cadastrar_terminal(self, terminal: Terminal) -> None:
        """
        Cadastra um novo terminal na planilha.

        Args:
            terminal (Terminal): Objeto Terminal a ser cadastrado.
        """
        # Gera o próximo ID automaticamente
        terminal.id = self._gerar_proximo_id()

        nova_linha = [
            terminal.id,
            terminal.nome,
            terminal.cidade,
            terminal.endereco,
            terminal.cnpj,
            terminal.cid_rota,
            f"{terminal.entrada[0]}, {terminal.entrada[1]}",
            f"{terminal.saida[0]}, {terminal.saida[1]}",
        ]
        self.worksheet.append_row(nova_linha)
