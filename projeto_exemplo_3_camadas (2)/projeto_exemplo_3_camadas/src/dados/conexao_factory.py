import mysql.connector

class ConexaoFactory:
    @staticmethod
    def criar_conexao():
        return mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="270209",  
            database="agenda_contatos"
        )