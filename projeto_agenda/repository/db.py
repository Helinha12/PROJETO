import mysql.connector  # type: ignore

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="270209",
        database="agenda_contatos"
    )

obter_conexao = conectar
