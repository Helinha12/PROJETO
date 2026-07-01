from dados.conexao_factory import ConexaoFactory

class ConexaoSingleton:
    _instancia_conexao = None

    @classmethod
    def obter_conexao(cls):
        if cls._instancia_conexao is None or not cls._instancia_conexao.is_connected():
            cls._instancia_conexao = ConexaoFactory.criar_conexao()
        return cls._instancia_conexao