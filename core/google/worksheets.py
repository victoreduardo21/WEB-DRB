import gspread

from core.google.spreadsheets.entregas import PlanilhaEntregas
from core.google.spreadsheets.motoristas import PlanilhaMotoristas
from core.google.spreadsheets.terminais import PlanilhaTerminais


gs = gspread.service_account(filename="credentials.json")
sh = gs.open_by_key(key="1B6o3EpkTbpmyM4vih12WLrqnFTD_5csQRQctUCbmLRs")


def get_motoristas():
    return PlanilhaMotoristas(sh)


def get_terminais():
    return PlanilhaTerminais(sh)


def get_entregas():
    return PlanilhaEntregas(sh)
