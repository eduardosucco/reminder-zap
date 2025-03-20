"""
Módulo que gerencia a conexão e operações no banco de dados SQLite.
"""
import sqlite3
from typing import List, Tuple

DB_NAME = "remedios.db"

def create_connection() -> sqlite3.Connection:
    """
    Cria ou retorna uma conexão com o banco de dados SQLite.
    """
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_table() -> None:
    """
    Cria a tabela 'remedios' se ainda não existir.
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS remedios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade TEXT NOT NULL,
            frequencia TEXT NOT NULL,
            data_inicio TEXT NOT NULL,
            data_fim TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def inserir_remedio(nome: str,
                    quantidade: str,
                    frequencia: str,
                    data_inicio: str,
                    data_fim: str) -> None:
    """
    Insere um novo registro de remédio na tabela.

    :param nome: Nome do remédio
    :param quantidade: Dose ou quantidade (ex: 5ml)
    :param frequencia: Frequência (ex: a cada 8h)
    :param data_inicio: Data de início (YYYY-MM-DD)
    :param data_fim: Data de término (YYYY-MM-DD)
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO remedios (nome, quantidade, frequencia, data_inicio, data_fim)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, quantidade, frequencia, data_inicio, data_fim))
    conn.commit()
    conn.close()

def listar_remedios() -> List[Tuple]:
    """
    Retorna todos os registros da tabela 'remedios'.

    :return: Lista de tuplas com os dados (id, nome, quantidade, frequencia, data_inicio, data_fim)
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM remedios")
    rows = cursor.fetchall()
    conn.close()
    return rows

def remover_remedio(remedio_id: int) -> None:
    """
    Remove um remédio pelo ID.

    :param remedio_id: ID do remédio a ser removido
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM remedios WHERE id = ?", (remedio_id,))
    conn.commit()
    conn.close()
