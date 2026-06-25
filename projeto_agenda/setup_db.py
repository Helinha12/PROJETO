#!/usr/bin/env python3
"""Script para executar init.sql automaticamente"""

import mysql.connector  # type: ignore
import os

def executar_init():
    print("=" * 60)
    print("EXECUTANDO init.sql")
    print("=" * 60)
    
    try:
        # Conectar sem especificar banco para criar a base
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="270209"
        )
        
        cursor = conn.cursor()
        print("✅ Conectado ao MySQL")
        
        # Ler arquivo init.sql
        script_path = os.path.join(os.path.dirname(__file__), "init.sql")
        if not os.path.exists(script_path):
            print(f"❌ Arquivo {script_path} não encontrado")
            return False
        
        with open(script_path, 'r', encoding='utf-8') as f:
            script = f.read()
        
        print(f"✅ Arquivo init.sql lido")
        
        # Executar comandos um por um
        for statement in script.split(';'):
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    print(f"✅ Executado: {statement[:50]}...")
                except Exception as e:
                    print(f"⚠️  Erro ao executar: {e}")
        
        conn.commit()
        conn.close()
        
        print("\n✅ init.sql executado com sucesso!")
        print("\nAgora você pode executar: python main.py")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {type(e).__name__}: {e}")
        print("\nVerifique:")
        print("- MySQL está rodando?")
        print("- Credenciais corretas em db.py?")
        return False

if __name__ == "__main__":
    executar_init()
