from dataclasses import dataclass, field
from typing import List, Optional
import json

from dominio.email import Email
from dominio.telefone import Telefone
from dominio.endereco import Endereco


@dataclass
class Contato:
    nome: str
    categoria: str
    telefones: List[Telefone] = field(default_factory=list)
    emails: List[Email] = field(default_factory=list)
    enderecos: List[Endereco] = field(default_factory=list)
    id: Optional[int] = None

    def to_db_tuple(self):
        # Serialize lists to JSON strings for storage
        telefones = [t.numero for t in self.telefones]
        emails = [e.endereco for e in self.emails]
        enderecos = [
            {
                'rua': e.rua,
                'numero': e.numero,
                'cidade': e.cidade,
                'estado': e.estado,
                'complemento': e.complemento
            }
            for e in self.enderecos
        ]

        return (
            self.nome,
            self.categoria,
            json.dumps(telefones, ensure_ascii=False),
            json.dumps(emails, ensure_ascii=False),
            json.dumps(enderecos, ensure_ascii=False),
        )

    @classmethod
    def from_db_row(cls, row):
        # Expecting row: (id, nome, categoria, telefone_json, email_json, endereco_json)
        import json

        _id, nome, categoria, telefones_json, emails_json, enderecos_json = row

        telefones = []
        emails = []
        enderecos = []

        try:
            tlist = json.loads(telefones_json) if telefones_json else []
            for n in tlist:
                telefones.append(Telefone(numero=n))
        except Exception:
            telefones = []

        try:
            elist = json.loads(emails_json) if emails_json else []
            for addr in elist:
                emails.append(Email(endereco=addr))
        except Exception:
            emails = []

        try:
            alist = json.loads(enderecos_json) if enderecos_json else []
            for d in alist:
                enderecos.append(Endereco(
                    rua=d.get('rua',''),
                    numero=d.get('numero'),
                    cidade=d.get('cidade'),
                    estado=d.get('estado'),
                    complemento=d.get('complemento')
                ))
        except Exception:
            enderecos = []

        return cls(nome=nome, categoria=categoria, telefones=telefones, emails=emails, enderecos=enderecos, id=_id)