from dados.Contato_repository import ContatoRepository
from dominio.Contato import Contato

class ContatoService:
    def __init__(self):
        self.repository = ContatoRepository()

    def cadastrar_contato(self, nome, categoria, telefones, emails, enderecos):
        if not nome.strip():
            raise ValueError("O campo Nome é obrigatório!")
        if not any(t.strip() for t in telefones):
            raise ValueError("Insira pelo menos um telefone válido.")

        novo_contato = Contato(nome=nome, categoria=categoria, telefones=telefones, emails=emails, enderecos=enderecos)
        self.repository.cadastrar(novo_contato)

    def listar_contatos(self, termo_pesquisa=""):
        return self.repository.listar_todos(termo_pesquisa)

    def excluir_contato(self, id_contato):
        if not id_contato:
            raise ValueError("Selecione um contato na tabela para excluir.")
        self.repository.deletar(id_contato)