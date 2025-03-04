class Motorista:
    def __init__(
        self, id: int, nome: str, cpf: str, cnh: str, cavalo: str, carreta: str
    ):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.cnh = cnh
        self.cavalo = cavalo
        self.carreta = carreta

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> "Motorista":
        return cls(
            id=int(data.get("Cod", 0)),
            nome=str(data.get("MOTORISTAS", "")).strip(),
            cpf=str(data.get("CPF", "")),
            cnh=str(data.get("CNH", "")),
            cavalo=str(data.get("CAVALO", "")),
            carreta=str(data.get("CARRETA", "")),
        )

    def __str__(self):
        return f"Motorista(id={self.id}, nome={self.nome}, cpf={self.cpf}, cnh={self.cnh}, cavalo={self.cavalo}, carreta={self.carreta})"
