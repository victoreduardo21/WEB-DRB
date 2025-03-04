import gspread
import os

from core.google.spreadsheets.entregas import PlanilhaEntregas
from core.google.spreadsheets.motoristas import PlanilhaMotoristas
from core.google.spreadsheets.terminais import PlanilhaTerminais

current_dir = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(current_dir, "credentials.json")

gs = gspread.service_account(filename=credentials_path)
sh = gs.open_by_key(key="1B6o3EpkTbpmyM4vih12WLrqnFTD_5csQRQctUCbmLRs")


def get_motoristas():
    return PlanilhaMotoristas(sh)


def get_terminais():
    return PlanilhaTerminais(sh)


def get_entregas():
    return PlanilhaEntregas(sh)
