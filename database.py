"""
Gerencia a conexão e operações no banco de dados SQLite.
Agora inclui a coluna 'telefone' para armazenar o WhatsApp de destino.
"""

import sqlite3
from typing import List, Tuple

DB_NAME = "remedios.db"

def create_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_table() -> None:
    conn = create_connection()
    cursor = conn.cursor()
    # Adicionamos o campo 'telefone' para armazenar o número de WhatsApp
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS remedios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade TEXT NOT NULL,
            frequencia TEXT NOT NULL,
            telefone TEXT NOT NULL,
            data_inicio TEXT NOT NULL,
            data_fim TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def inserir_remedio(nome: str,
                    quantidade: str,
                    frequencia: str,
                    telefone: str,
                    data_inicio: str,
                    data_fim: str) -> None:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO remedios (nome, quantidade, frequencia, telefone, data_inicio, data_fim)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, quantidade, frequencia, telefone, data_inicio, data_fim))
    conn.commit()
    conn.close()

def listar_remedios() -> List[Tuple]:
    """
    Retorna todos os registros da tabela 'remedios'.
    Cada linha terá 7 colunas: (id, nome, quantidade, frequencia, telefone, data_inicio, data_fim)
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM remedios")
    rows = cursor.fetchall()
    conn.close()
    return rows

def remover_remedio(remedio_id: int) -> None:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM remedios WHERE id = ?", (remedio_id,))
    conn.commit()
    conn.close()
