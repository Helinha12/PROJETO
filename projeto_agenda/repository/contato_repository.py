from repository.db import conectar
import json
from dominio.contato import Contato


class ContatoRepository:

    @staticmethod
    def criar_tabela():

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contatos(
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                categoria VARCHAR(100) NOT NULL,
                telefone JSON,
                email JSON,
                endereco JSON
            )
        """)

        conn.commit()
        conn.close()

    @staticmethod
    def salvar(contato: Contato):
        conn = conectar()
        cursor = conn.cursor()

        ContatoRepository.criar_tabela()

        if contato.id:
            cursor.execute(
                """
                UPDATE contatos SET nome = %s, categoria = %s, telefone = %s, email = %s, endereco = %s
                WHERE id = %s
                """,
                contato.to_db_tuple() + (contato.id,)
            )
            last_id = contato.id
        else:
            cursor.execute(
                """
                INSERT INTO contatos (nome, categoria, telefone, email, endereco)
                VALUES (%s, %s, %s, %s, %s)
                """,
                contato.to_db_tuple()
            )
            last_id = cursor.lastrowid

        conn.commit()
        conn.close()
        return last_id

    @staticmethod
    def remover(contato_id: int):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM contatos WHERE id = %s", (contato_id,))

        conn.commit()
        conn.close()

    @staticmethod
    def listar_todos():
        # ensure table exists and schema is up-to-date
        ContatoRepository.criar_tabela()

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT id, nome, categoria_id, telefone, email, endereco FROM contatos")
        rows = cursor.fetchall()
        conn.close()

        contatos = []
        for row in rows:
            contatos.append(Contato.from_db_row(row))

        return contatos