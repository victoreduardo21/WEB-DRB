class Entrega:
    def __init__(
        self,
        id_motorista: int,
        container: str,
        motorista: str,
        cpf: str,
        cnh: str,
        cavalo: str,
        carreta: str,
        janela: str,
    ):
        self.id_motorista = id_motorista
        self.container = container
        self.motorista = motorista
        self.cpf = cpf
        self.cnh = cnh
        self.cavalo = cavalo
        self.carreta = carreta
        self.janela = janela

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> "Entrega":
        return cls(
            id_motorista=int(data.get("Cod", 0)),
            container=str(data.get("CONTAINER", "")).strip(),
            motorista=str(data.get("MOTORISTAS", "")).strip(),
            cpf=str(data.get("CPF", "")).strip(),
            cnh=str(data.get("CNH", "")).strip(),
            cavalo=str(data.get("CAVALO", "")).strip(),
            carreta=str(data.get("CARRETA", "")).strip(),
            janela=str(data.get("JANELA", "")).strip(),
        )

    def __str__(self):
        return (
            f"Entrega(id_motorista={self.id_motorista}, container={self.container}, "
            f"motorista={self.motorista}, cpf={self.cpf}, cnh={self.cnh}, "
            f"cavalo={self.cavalo}, carreta={self.carreta}, janela={self.janela})"
        )
