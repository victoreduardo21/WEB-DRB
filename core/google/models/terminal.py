class Terminal:
    def __init__(
        self,
        id: int | None,
        nome: str,
        cidade: str,
        endereco: str,
        cnpj: str,
        cid_rota: str,
        entrada: tuple[float, float],
        saida: tuple[float | None, float | None],
    ):
        self.id = id
        self.nome = nome
        self.cidade = cidade
        self.endereco = endereco
        self.cnpj = cnpj
        self.cid_rota = cid_rota
        self.entrada = entrada
        self.saida = saida

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> "Terminal":
        def parse_geopoint(value: str) -> tuple[float, float]:
            try:
                lat, lon = map(float, value.split(", "))
                return lat, lon
            except (ValueError, AttributeError):
                return None, None

        try:
            id_terminal = int(data.get("ID_TERMINAL", 0))
        except (ValueError, TypeError):
            id_terminal = None

        return cls(
            id=id_terminal,
            nome=str(data.get("TERMINAL", "")).strip(),
            cidade=str(data.get("CIDADE", "")).strip(),
            endereco=str(data.get("ENDEREÇO", "")).strip(),
            cnpj=str(data.get("CNPJ", "")).strip(),
            cid_rota=str(data.get("CID_ROTA", "")).strip(),
            entrada=parse_geopoint(data.get("ENTRADA", "0, 0")),
            saida=parse_geopoint(data.get("SAIDA", "0, 0")),
        )

    def __str__(self):
        return f"Terminal(id={self.id}, nome={self.nome}, cidade={self.cidade}, endereco={self.endereco}, cnpj={self.cnpj}, cid_rota={self.cid_rota}, entrada={self.entrada}, saida={self.saida})"
