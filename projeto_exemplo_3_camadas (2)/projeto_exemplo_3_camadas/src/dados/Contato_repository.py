from dados.conexao_singleton import ConexaoSingleton
from dominio.Contato import Contato

class ContatoRepository:
    def __init__(self):
        self.db = ConexaoSingleton.obter_conexao()
        
    def cadastrar(self, contato: Contato):
        cursor = self.db.cursor()
        sql_contato = "INSERT INTO contatos (nome, categoria) VALUES (%s, %s)"
        cursor.execute(sql_contato, (contato.nome, contato.categoria))
        contato_id = cursor.lastrowid
        
        for tel in contato.telefones:
            if tel.strip():
                cursor.execute("INSERT INTO telefones (contato_id, telefone) VALUES (%s, %s)", (contato_id, tel))
                
        for email in contato.emails:
            if email.strip():
                cursor.execute("INSERT INTO emails (contato_id, email) VALUES (%s, %s)", (contato_id, email))
        
        for end in contato.enderecos:
            sql_end = """
                INSERT INTO enderecos (contato_id, rua, numero, bairro, cidade, estado, cep) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_end, (
                contato_id, 
                end['rua'], 
                end['numero'], 
                end['bairro'], 
                end['cidade'], 
                end['estado'], 
                end['cep']
            ))
                
        self.db.commit()
        cursor.close()

    def listar_todos(self, termo_pesquisa=""):
        cursor = self.db.cursor(dictionary=True)
        if termo_pesquisa:
            cursor.execute("SELECT * FROM contatos WHERE nome LIKE %s ORDER BY nome", (f"%{termo_pesquisa}%",))
        else:
            cursor.execute("SELECT * FROM contatos ORDER BY nome")
            
        lista_contatos = cursor.fetchall()
        contatos_completos = []
        
        for c in lista_contatos:
            c_id = c['id']
            
            cursor.execute("SELECT telefone FROM telefones WHERE contato_id = %s", (c_id,))
            tels = [t['telefone'] for t in cursor.fetchall()]
            
            cursor.execute("SELECT email FROM emails WHERE contato_id = %s", (c_id,))
            ems = [e['email'] for e in cursor.fetchall()]
            
            cursor.execute("SELECT rua, numero, bairro, cidade, estado, cep FROM enderecos WHERE contato_id = %s", (c_id,))
            ends_completos = cursor.fetchall()
            ends_formatados = []
            for end in ends_completos:
                texto = f"{end['rua']}, {end['numero']} - {end['bairro']}, {end['cidade']}/{end['estado']} (CEP: {end['cep']})"
                ends_formatados.append(texto)
            
            contatos_completos.append(Contato(c_id, c['nome'], c['categoria'], tels, ems, ends_formatados))
            
        cursor.close()
        return contatos_completos

    def deletar(self, id_contato):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM contatos WHERE id = %s", (id_contato,))
        self.db.commit()
        cursor.close()