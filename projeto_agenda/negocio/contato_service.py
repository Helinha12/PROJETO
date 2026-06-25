from repository.contato_repository import ContatoRepository


class ContatoService:

    def __init__(self):
        self.repository = ContatoRepository()
    
    def salvar(self, contato):
        return ContatoRepository.salvar(contato)

    def listar_todos(self):
        return ContatoRepository.listar_todos()
    
    def remover(self, contato_id: int):
        return ContatoRepository.remover(contato_id)

    def atualizar(self, contato: object):
        return ContatoRepository.salvar(contato)