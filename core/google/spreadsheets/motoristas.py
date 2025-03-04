from gspread import Spreadsheet
from typing import List, Optional
import re

from core.google.models.motorista import Motorista


class PlanilhaMotoristas:
    def __init__(self, spreadsheet: Spreadsheet):
        """
        Inicializa a classe PlanilhaMotoristas com a planilha do Google Sheets.

        Args:
            spreadsheet (Spreadsheet): Objeto da planilha do Google Sheets.
        """
        self.spreadsheet = spreadsheet
        self.worksheet = spreadsheet.worksheet(title="CADASTRO_MOTORISTAS")

    def _gerar_proximo_id(self) -> int:
        """
        Gera o próximo ID disponível para um novo motorista.

        Returns:
            int: Próximo ID disponível.
        """
        dados = self.worksheet.get_all_records()
        if not dados:
            return 1
        ids = [int(motorista.get("Cod", 0)) for motorista in dados]
        return max(ids) + 1

    def _limpar_cpf(self, cpf: str) -> str:
        """
        Remove máscaras (pontos e hífens) do CPF.

        Args:
            cpf (str): CPF a ser limpo.

        Returns:
            str: CPF sem máscaras.
        """
        return re.sub(r"[^0-9]", "", cpf)

    def buscar_todos_motoristas(self) -> List[Motorista]:
        """
        Retorna uma lista de todos os motoristas cadastrados na planilha.

        Returns:
            List[Motorista]: Lista de objetos Motorista.
        """
        dados = self.worksheet.get_all_records()
        return [Motorista.from_dict(motorista) for motorista in dados]

    def buscar_motorista(self, cpf: str, placa_cavalo: str) -> Optional[Motorista]:
        """
        Busca um motorista pelo CPF e pela placa do cavalo.

        Args:
            cpf (str): CPF do motorista.
            placa_cavalo (str): Placa do cavalo associado ao motorista.

        Returns:
            Optional[Motorista]: Objeto Motorista encontrado, ou None se não for encontrado.
        """
        cpf_limpo = self._limpar_cpf(cpf)
        dados = self.worksheet.get_all_records()

        for motorista in dados:
            cpf_motorista = self._limpar_cpf(str(motorista.get("CPF", "")))
            cavalo_motorista = str(motorista.get("CAVALO", "")).strip()

            if cpf_motorista == cpf_limpo and cavalo_motorista == placa_cavalo:
                return Motorista.from_dict(motorista)

        return None

    def cadastrar_motorista(self, motorista: Motorista) -> None:
        """
        Cadastra um novo motorista na planilha.

        Args:
            motorista (Motorista): Objeto Motorista a ser cadastrado.
        """
        # Gera o próximo ID automaticamente
        motorista.id = self._gerar_proximo_id()

        nova_linha = [
            motorista.id,
            motorista.nome,
            motorista.cpf,
            motorista.cnh,
            motorista.cavalo,
            motorista.carreta,
        ]
        self.worksheet.append_row(nova_linha)
