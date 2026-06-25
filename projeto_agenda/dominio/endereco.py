from dataclasses import dataclass


@dataclass
class Endereco:
    rua: str
    numero: str | None = None
    cidade: str | None = None
    estado: str | None = None
    complemento: str | None = None