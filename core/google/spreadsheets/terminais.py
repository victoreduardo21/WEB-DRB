from gspread import Spreadsheet
from typing import List
import re

from core.google.models.terminal import Terminal


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

        ids = []
        for terminal in dados:
            id_terminal = terminal.get("ID_TERMINAL", "")
            # Verifica se o campo não está vazio e pode ser convertido para int
            if id_terminal and str(id_terminal).strip().isdigit():
                ids.append(int(id_terminal))

        # Se nenhum ID válido for encontrado, retorna 1
        if not ids:
            return 1

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
            if self._limpar_cnpj(str(terminal.get("CNPJ", ""))) == cnpj_limpo
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
            terminal.raio,
            f"{terminal.entrada[0]}, {terminal.entrada[1]}" if terminal.entrada else "",
            f"{terminal.saida[0]}, {terminal.saida[1]}" if terminal.saida else "",
        ]

        self.worksheet.append_row(nova_linha)
