class Contato:
    def __init__(self, id=None, nome="", categoria="Pessoal", telefones=None, emails=None, enderecos=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.telefones = telefones if telefones is not None else []
        self.emails = emails if emails is not None else []
        self.enderecos = enderecos if enderecos is not None else []